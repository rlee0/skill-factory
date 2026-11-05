"""Shared semantics for behavioral evaluation evidence and outcomes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

RUBRIC_JUDGE_VOTES = 3


@dataclass(frozen=True)
class AdjudicatedScores:
    treatment: list[bool]
    baseline: list[bool] | None


def assess_case(
    definition: dict[str, Any],
    result: dict[str, Any],
    *,
    adjudicated_scores_by_repeat: dict[int, AdjudicatedScores] | None = None,
    require_recorded: bool = True,
) -> tuple[dict[str, Any], list[str]]:
    """Derive a case outcome from repeat evidence and check any recorded summaries.

    Callers may provide validated human-adjudicated scores for release decisions. The
    returned result keeps the automated score fields while deriving pass/fail from
    the adjudicated scores. Set ``require_recorded=False`` while constructing a result
    from raw judge votes; validation callers should require the serialized fields.
    """
    case_id = definition.get("id", result.get("case", "unknown"))
    prefix = f"evaluation case {case_id!r}"
    errors: list[str] = []

    def issue(message: str) -> None:
        errors.append(f"{prefix} {message}")

    kind = definition.get("kind")
    criteria = definition.get("success_criteria")
    expected_activation = definition.get("expected_activation")
    skill_name = definition.get("skill", result.get("skill"))
    for field in ("kind", "critical", "expected_activation"):
        if field in result and result[field] != definition.get(field):
            issue(f"field {field!r} does not match the case definition")
        elif require_recorded and field not in result:
            issue(f"must record field {field!r}")
    repeats = result.get("repeats")
    run_evidence = result.get("run_evidence")
    if kind not in {"trigger", "task"}:
        issue("has an unsupported case kind")
        kind = "trigger"
    if not isinstance(criteria, list) or not criteria or not all(isinstance(item, str) for item in criteria):
        issue("has invalid success criteria")
        criteria = []
    if not isinstance(expected_activation, bool):
        issue("has an invalid activation expectation")
        expected_activation = False
    if not isinstance(skill_name, str) or not skill_name:
        issue("has no target skill name")
        skill_name = ""
    if not isinstance(run_evidence, list):
        issue("needs repeat-level evidence")
        run_evidence = []
    if not isinstance(repeats, int) or isinstance(repeats, bool) or repeats < 1:
        issue("has an invalid repeat count")
        repeats = len(run_evidence)
    if len(run_evidence) != repeats:
        issue("needs complete repeat-level evidence")

    majority = RUBRIC_JUDGE_VOTES // 2 + 1
    normalized_runs: list[dict[str, Any]] = []
    seen_repeats: set[int] = set()
    loaded_summary: set[str] = set()
    baseline_summary: set[str] = set()
    target_runs = 0
    activation_errors = 0
    runtime_errors = 0
    rubric_failures = 0
    safety_observed = False
    baseline_passes = 0
    all_repeats_passed = bool(run_evidence) and len(run_evidence) == repeats

    for index, raw_run in enumerate(run_evidence, start=1):
        if not isinstance(raw_run, dict):
            issue(f"has malformed evidence for repeat {index}")
            runtime_errors += 1
            all_repeats_passed = False
            continue
        run = dict(raw_run)
        if require_recorded and "repeat" not in run:
            issue(f"must record the repeat identifier for repeat {index}")
        repeat = run.get("repeat", index)
        if not isinstance(repeat, int) or isinstance(repeat, bool) or not 1 <= repeat <= repeats or repeat in seen_repeats:
            issue(f"has invalid repeat identifiers for repeat {index}")
        if isinstance(repeat, int) and not isinstance(repeat, bool):
            seen_repeats.add(repeat)
        run["repeat"] = repeat

        treatment_status = run.get("treatment_status")
        if require_recorded and treatment_status != "completed":
            issue(f"has incomplete treatment evidence for repeat {index}")
        if require_recorded and run.get("judge_status") != "completed":
            issue(f"has incomplete judge evidence for repeat {index}")
        loaded = run.get("treatment_loaded_skill_ids")
        if not isinstance(loaded, list) or not all(isinstance(item, str) for item in loaded):
            issue(f"must record loaded skill IDs for repeat {index}")
            loaded = []
            run["treatment_loaded_skill_ids"] = loaded
        loaded_summary.update(loaded)
        target_loaded = skill_name in loaded
        target_runs += int(target_loaded)
        activation = target_loaded == expected_activation
        recorded_activation = run.get("activation_passed")
        if treatment_status == "completed":
            if not isinstance(recorded_activation, bool):
                issue(f"must record activation for repeat {index}")
        if recorded_activation is not None and recorded_activation != activation:
            issue(f"has inconsistent repeat-level activation evidence for repeat {index}")
        if result.get("status") == "passed" and treatment_status == "completed" and not activation:
            issue(f"records a false activation for repeat {index}")
        run["activation_passed"] = activation if treatment_status == "completed" else recorded_activation
        if run["activation_passed"] is False:
            activation_errors += 1

        votes = run.get("judge_votes")
        valid_votes: list[dict[str, Any]] = []
        if not isinstance(votes, list):
            issue(f"needs {RUBRIC_JUDGE_VOTES} rubric judge votes for repeat {index}")
            votes = []
        elif len(votes) != RUBRIC_JUDGE_VOTES:
            issue(f"needs {RUBRIC_JUDGE_VOTES} rubric judge votes for repeat {index}")
        vote_safety_observed = any(
            isinstance(vote, dict) and vote.get("safety_regression") is True
            for vote in votes
        )
        recorded_safety = run.get("safety_regression")
        repeat_safety_observed = vote_safety_observed or recorded_safety is True
        if repeat_safety_observed:
            issue(f"records a safety regression for repeat {index}")
        if require_recorded and type(recorded_safety) is not bool:
            issue(f"must record safety evidence for repeat {index}")
        elif isinstance(recorded_safety, bool) and recorded_safety is not vote_safety_observed:
            issue(f"safety result does not conservatively aggregate judge votes for repeat {index}")
        for vote in votes:
            if not isinstance(vote, dict) or vote.get("judge_status") != "completed":
                issue(f"has incomplete rubric judge votes for repeat {index}")
                continue
            treatment_vote = vote.get("treatment_scores")
            baseline_vote = vote.get("baseline_scores")
            safety_vote = vote.get("safety_regression")
            if (not isinstance(treatment_vote, list) or len(treatment_vote) != len(criteria)
                    or not all(type(value) is bool for value in treatment_vote)):
                issue(f"has invalid treatment votes for repeat {index}")
                continue
            if kind == "task":
                if (not isinstance(baseline_vote, list) or len(baseline_vote) != len(criteria)
                        or not all(type(value) is bool for value in baseline_vote)):
                    issue(f"has invalid baseline votes for repeat {index}")
                    continue
            elif baseline_vote is not None:
                issue(f"has unexpected baseline votes for repeat {index}")
                continue
            if type(safety_vote) is not bool:
                issue(f"has invalid safety votes for repeat {index}")
                continue
            valid_votes.append(vote)

        votes_complete = len(valid_votes) == RUBRIC_JUDGE_VOTES
        runtime_incomplete = treatment_status != "completed" or run.get("judge_status") != "completed"
        if kind == "task" and run.get("baseline_status") != "completed":
            runtime_incomplete = True
        if not votes_complete:
            runtime_incomplete = True
        if runtime_incomplete:
            runtime_errors += 1
            all_repeats_passed = False
            if require_recorded:
                issue(f"has incomplete runtime evidence for repeat {index}")

        treatment_scores: list[bool] | None = None
        baseline_scores: list[bool] | None = None
        safety_regression = repeat_safety_observed
        if votes_complete:
            treatment_scores = [
                sum(vote["treatment_scores"][criterion] for vote in valid_votes) >= majority
                for criterion in range(len(criteria))
            ]
            baseline_scores = (
                [
                    sum(vote["baseline_scores"][criterion] for vote in valid_votes) >= majority
                    for criterion in range(len(criteria))
                ]
                if kind == "task" else None
            )
            for field, expected in (
                ("treatment_scores", treatment_scores),
                ("baseline_scores", baseline_scores),
            ):
                if field not in run:
                    if require_recorded:
                        issue(f"must record {field} for repeat {index}")
                elif run[field] != expected:
                    issue(f"{field.replace('_', ' ')} do not match judge majority for repeat {index}")
            run["treatment_scores"] = treatment_scores
            run["baseline_scores"] = baseline_scores
            run["safety_regression"] = safety_regression
            safety_observed = safety_observed or safety_regression
        else:
            for field in ("treatment_scores", "baseline_scores"):
                run.setdefault(field, None)
            run["safety_regression"] = safety_regression
            safety_observed = safety_observed or safety_regression

        baseline_status = run.get("baseline_status")
        baseline_ids = run.get("baseline_loaded_skill_ids")
        if kind == "task":
            if baseline_status != "completed":
                issue(f"has incomplete baseline evidence for repeat {index}")
                runtime_incomplete = True
            if baseline_status == "completed":
                if not isinstance(baseline_ids, list) or not all(isinstance(item, str) for item in baseline_ids):
                    issue(f"must record baseline skill IDs for repeat {index}")
                    baseline_ids = []
                    run["baseline_loaded_skill_ids"] = baseline_ids
                baseline_summary.update(baseline_ids)
                if not isinstance(run.get("baseline_scores"), list):
                    runtime_incomplete = True
        elif baseline_status is not None or baseline_ids is not None or run.get("baseline_scores") is not None:
            issue(f"must not include baseline evidence for trigger repeat {index}")

        effective_treatment, effective_baseline = treatment_scores, baseline_scores
        adjudicated = (adjudicated_scores_by_repeat or {}).get(repeat)
        if adjudicated is not None:
            effective_treatment = adjudicated.treatment
            effective_baseline = adjudicated.baseline
        automatic_treatment_passed = False
        effective_treatment_passed = False
        baseline_passed = all(baseline_scores) if baseline_scores is not None else None
        if treatment_scores is not None:
            automatic_treatment_passed = all(treatment_scores)
            effective_treatment = effective_treatment or treatment_scores
            if kind == "task":
                if baseline_scores is not None and effective_baseline is None:
                    effective_baseline = baseline_scores
                policy = definition.get("comparison_policy")
                if effective_baseline is not None:
                    treatment_count = sum(effective_treatment)
                    baseline_count = sum(effective_baseline)
                    if policy == "uplift":
                        effective_treatment_passed = all(effective_treatment) and treatment_count > baseline_count
                        automatic_treatment_passed = (
                            automatic_treatment_passed and sum(treatment_scores) > sum(baseline_scores or [])
                        )
                    elif policy == "no-regression":
                        effective_treatment_passed = all(effective_treatment) and treatment_count >= baseline_count
                        automatic_treatment_passed = (
                            automatic_treatment_passed and sum(treatment_scores) >= sum(baseline_scores or [])
                        )
                    else:
                        issue("has an unsupported task comparison policy")
                else:
                    effective_treatment_passed = False
                    automatic_treatment_passed = False
            else:
                effective_treatment_passed = all(effective_treatment)
        if treatment_scores is not None:
            if "treatment_passed" in run and run["treatment_passed"] is not automatic_treatment_passed:
                issue(f"has inconsistent treatment outcome for repeat {index}")
            if "baseline_passed" in run and run["baseline_passed"] is not baseline_passed:
                issue(f"has inconsistent baseline outcome for repeat {index}")
            run["treatment_passed"] = automatic_treatment_passed
            run["baseline_passed"] = baseline_passed
        if treatment_scores is not None and not automatic_treatment_passed:
            rubric_failures += 1

        repeat_passed = (
            not runtime_incomplete
            and run["activation_passed"] is True
            and effective_treatment_passed
            and safety_regression is False
        )
        if not repeat_passed:
            all_repeats_passed = False
        normalized_runs.append(run)

    expected_status = "passed" if all_repeats_passed else "failed"
    if "status" in result and result["status"] != expected_status:
        if result["status"] == "failed" and expected_status == "passed":
            issue("failed case has no failing repeat")
        else:
            issue("has a failed repeat in a passing result")
    elif require_recorded and "status" not in result:
        issue("must record a case status")

    normalized = dict(result)
    normalized.update({
        "status": expected_status,
        "repeats": len(normalized_runs),
        "run_evidence": normalized_runs,
        "activation_errors": activation_errors,
        "runtime_errors": runtime_errors,
        "rubric_failures": rubric_failures,
        "runs_with_target_skill": target_runs,
        "loaded_skill_ids": sorted(loaded_summary),
        "safety_regression": safety_observed,
    })
    if kind == "task":
        normalized.update({
            "baseline_repeats": len(normalized_runs),
            "baseline_loaded_skill_ids": sorted(baseline_summary),
            "baseline_passes": sum(run.get("baseline_passed") is True for run in normalized_runs),
        })
    else:
        normalized.update({
            "baseline_repeats": None,
            "baseline_loaded_skill_ids": None,
            "baseline_passes": None,
        })

    summary_fields = [
        "repeats", "activation_errors", "runtime_errors", "rubric_failures",
        "runs_with_target_skill", "loaded_skill_ids", "safety_regression",
    ]
    if kind == "task":
        summary_fields.extend(("baseline_repeats", "baseline_loaded_skill_ids", "baseline_passes"))
    for field in summary_fields:
        if field in result and result[field] != normalized[field]:
            issue(f"summary field {field!r} does not match repeat evidence")
        elif require_recorded and field not in result:
            issue(f"must record summary field {field!r}")

    return normalized, errors
