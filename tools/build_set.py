#!/usr/bin/env python3
"""Build a consumer archive for one skill set."""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from .check_repo import ROOT, read_json, validate_repo
    from .evaluation_contract import RUBRIC_JUDGE_VOTES
except ImportError:  # Direct script execution.
    from check_repo import ROOT, read_json, validate_repo
    from evaluation_contract import RUBRIC_JUDGE_VOTES


def validate_human_adjudication(
    adjudication: Any,
    treatment_scores: list[bool],
    baseline_scores: list[bool] | None,
    criteria_count: int,
    has_baseline: bool,
    case_id: str,
    target: str,
) -> tuple[list[bool], list[bool] | None, list[str]]:
    errors: list[str] = []
    if not isinstance(adjudication, dict):
        return treatment_scores, baseline_scores, [
            f"evaluation case {case_id!r} has malformed human adjudication for {target!r}"
        ]
    required = {
        "reviewer", "reviewed_at", "evidence", "treatment_scores", "baseline_scores",
        "rationale_by_criterion",
    }
    if set(adjudication) != required:
        errors.append(f"evaluation case {case_id!r} has malformed human adjudication fields for {target!r}")
    reviewer = adjudication.get("reviewer")
    evidence = adjudication.get("evidence")
    reviewed_at = adjudication.get("reviewed_at")
    if not isinstance(reviewer, str) or not reviewer.strip():
        errors.append(f"evaluation case {case_id!r} human adjudication must identify a reviewer for {target!r}")
    if not isinstance(evidence, str) or not evidence.strip():
        errors.append(f"evaluation case {case_id!r} human adjudication must cite reviewed evidence for {target!r}")
    timestamp_valid = False
    if isinstance(reviewed_at, str) and reviewed_at.strip():
        try:
            parsed = datetime.fromisoformat(reviewed_at.replace("Z", "+00:00"))
            timestamp_valid = parsed.tzinfo is not None and parsed.utcoffset() is not None
        except ValueError:
            pass
    if not timestamp_valid:
        errors.append(f"evaluation case {case_id!r} human adjudication needs a timezone-aware reviewed_at for {target!r}")

    human_treatment = adjudication.get("treatment_scores")
    if (not isinstance(human_treatment, list) or len(human_treatment) != criteria_count
            or not all(type(item) is bool for item in human_treatment)):
        errors.append(f"evaluation case {case_id!r} human treatment scores are invalid for {target!r}")
        human_treatment = None
    human_baseline = adjudication.get("baseline_scores")
    if has_baseline:
        if (not isinstance(human_baseline, list) or len(human_baseline) != criteria_count
                or not all(type(item) is bool for item in human_baseline)):
            errors.append(f"task case {case_id!r} human baseline scores are invalid for {target!r}")
            human_baseline = None
    elif human_baseline is not None:
        errors.append(f"trigger case {case_id!r} human adjudication must not include baseline scores for {target!r}")

    rationale = adjudication.get("rationale_by_criterion")
    if (not isinstance(rationale, dict) or set(rationale) != {"treatment", "baseline"}
            or not isinstance(rationale.get("treatment"), dict)
            or not isinstance(rationale.get("baseline"), dict)):
        errors.append(f"evaluation case {case_id!r} human adjudication needs treatment/baseline rationale maps for {target!r}")
        rationale = {"treatment": {}, "baseline": {}}

    score_groups = [
        ("treatment", treatment_scores, human_treatment, rationale["treatment"]),
    ]
    if has_baseline:
        score_groups.append(("baseline", baseline_scores, human_baseline, rationale["baseline"]))
    elif rationale["baseline"]:
        errors.append(f"trigger case {case_id!r} human adjudication has unexpected baseline rationales for {target!r}")

    for label, automatic, human, reason_map in score_groups:
        if not isinstance(reason_map, dict):
            errors.append(f"evaluation case {case_id!r} human {label} rationales are invalid for {target!r}")
            continue
        differences: set[str] = set()
        if human is not None and len(automatic) == criteria_count:
            differences = {
                str(index + 1)
                for index, (automated, adjudicated) in enumerate(zip(automatic, human))
                if automated is not adjudicated
            }
        for key, reason in reason_map.items():
            if (not isinstance(key, str) or not key.isdigit() or not 1 <= int(key) <= criteria_count
                    or not isinstance(reason, str) or not reason.strip()):
                errors.append(f"evaluation case {case_id!r} has invalid human {label} rationale for {target!r}")
        for key in differences - set(reason_map):
            errors.append(f"evaluation case {case_id!r} human {label} override for criterion {key} requires a rationale for {target!r}")

    if errors or human_treatment is None or (has_baseline and human_baseline is None):
        return treatment_scores, baseline_scores, errors
    return human_treatment, human_baseline, []


def validate_report(report_path: Path, set_name: str, version: str, targets: list[str]) -> list[str]:
    errors: list[str] = []
    if not report_path.is_file():
        return [f"missing passing evaluation report: {report_path.relative_to(ROOT)}"]
    report = read_json(report_path, errors)
    if report is None:
        return errors
    if report.get("set") != set_name:
        errors.append("evaluation report set does not match the release set")
    if report.get("version") != version:
        errors.append("evaluation report version does not match set.json")
    if report.get("status") != "passed":
        errors.append("evaluation report status must be 'passed'")
    if not isinstance(report.get("generated_at"), str) or not report["generated_at"].strip():
        errors.append("evaluation report must record generated_at")
    baseline_definition = report.get("baseline_definition")
    if not isinstance(baseline_definition, str) or not baseline_definition.strip():
        errors.append("evaluation report must define its runtime baseline")
    else:
        definition = baseline_definition.casefold()
        if "without" not in definition or "remain" not in definition or not any(
            marker in definition for marker in ("native", "runtime-provided", "opencode-provided")
        ):
            errors.append("evaluation report baseline must omit the candidate set and retain native runtime capabilities")

    runtimes = report.get("runtimes")
    if not isinstance(runtimes, list):
        errors.append("evaluation report runtimes must be an array")
        return errors
    valid_runtime_entries = [
        entry for entry in runtimes
        if isinstance(entry, dict) and isinstance(entry.get("name"), str) and entry["name"].strip()
    ]
    by_name = {entry["name"]: entry for entry in valid_runtime_entries}
    if len(by_name) != len(runtimes):
        errors.append("evaluation report contains malformed or duplicate runtime entries")
    extra_runtimes = set(by_name) - set(targets)
    if extra_runtimes:
        errors.append(f"evaluation report contains undeclared runtimes: {', '.join(sorted(extra_runtimes))}")
    set_root = ROOT / "sets" / set_name
    expected_cases: dict[str, dict[str, Any]] = {}
    descriptor = json.loads((set_root / "set.json").read_text(encoding="utf-8"))
    for member in descriptor["skills"]:
        cases_path = set_root / member["path"] / "evals" / "cases.json"
        case_doc = json.loads(cases_path.read_text(encoding="utf-8"))
        for case in case_doc["cases"]:
            expected_cases[case["id"]] = {"definition": case, "skill": member["name"]}
    for target in targets:
        entry = by_name.get(target)
        if entry is None:
            errors.append(f"evaluation report has no result for target runtime {target!r}")
            continue
        for field in ("version", "model"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                errors.append(f"evaluation result for {target!r} must record {field}")
        if entry.get("status") != "passed":
            errors.append(f"evaluation result for {target!r} must have status 'passed'")
        cases = entry.get("cases")
        if not isinstance(cases, list) or not cases:
            errors.append(f"evaluation result for {target!r} must include case results")
            continue
        actual_cases = {case.get("id"): case for case in cases if isinstance(case, dict)}
        if len(actual_cases) != len(cases):
            errors.append(f"evaluation result for {target!r} has malformed or duplicate case results")
        missing_cases = set(expected_cases) - set(actual_cases)
        if missing_cases:
            errors.append(f"evaluation result for {target!r} is missing cases: {', '.join(sorted(missing_cases))}")
        for case in cases:
            if not isinstance(case, dict) or case.get("status") not in {"passed", "failed"}:
                errors.append(f"evaluation case result for {target!r} needs a passed/failed status")
                continue
            case_id = case.get("id")
            expected = expected_cases.get(case_id)
            if expected is None:
                errors.append(f"evaluation result for {target!r} contains unknown case {case_id!r}")
                continue
            definition = expected["definition"]
            if case.get("critical") is not definition["critical"]:
                errors.append(f"evaluation case {case_id!r} has the wrong criticality for {target!r}")
            if case.get("expected_activation") is not definition["expected_activation"]:
                errors.append(f"evaluation case {case_id!r} has the wrong activation expectation for {target!r}")
            repeats = case.get("repeats")
            if not isinstance(repeats, int) or isinstance(repeats, bool) or repeats < definition["repeats"]:
                errors.append(f"evaluation case {case_id!r} has too few repeats for {target!r}")
                repeats = 0
            loaded_skills = case.get("loaded_skill_ids")
            if not isinstance(loaded_skills, list) or not all(isinstance(item, str) for item in loaded_skills):
                errors.append(f"evaluation case {case_id!r} must list observed skill IDs for {target!r}")
                loaded_skills = []
            target_skill = expected["skill"]
            runs_with_target = case.get("runs_with_target_skill")
            if not isinstance(runs_with_target, int) or isinstance(runs_with_target, bool) or not 0 <= runs_with_target <= repeats:
                errors.append(f"evaluation case {case_id!r} must record valid target-skill activation counts for {target!r}")
            run_evidence = case.get("run_evidence")
            if not isinstance(run_evidence, list) or len(run_evidence) != repeats:
                errors.append(f"evaluation case {case_id!r} needs complete repeat-level evidence for {target!r}")
                run_evidence = []
            observed_loaded: set[str] = set()
            observed_baseline: set[str] = set()
            target_runs = 0
            safety_observed = False
            seen_repeats: set[int] = set()
            effective_scores_by_repeat: dict[int, list[bool]] = {}
            for run in run_evidence:
                if not isinstance(run, dict):
                    errors.append(f"evaluation case {case_id!r} has malformed repeat-level evidence for {target!r}")
                    continue
                repeat_number = run.get("repeat")
                if not isinstance(repeat_number, int) or isinstance(repeat_number, bool) or not 1 <= repeat_number <= repeats or repeat_number in seen_repeats:
                    errors.append(f"evaluation case {case_id!r} has invalid repeat identifiers for {target!r}")
                else:
                    seen_repeats.add(repeat_number)
                if run.get("treatment_status") != "completed":
                    errors.append(f"evaluation case {case_id!r} has missing treatment evidence for {target!r}")
                treatment_ids = run.get("treatment_loaded_skill_ids")
                if not isinstance(treatment_ids, list) or not all(isinstance(item, str) for item in treatment_ids):
                    errors.append(f"evaluation case {case_id!r} must record repeat-level loaded skill IDs for {target!r}")
                    treatment_ids = []
                observed_loaded.update(treatment_ids)
                target_was_loaded = target_skill in treatment_ids
                target_runs += int(target_was_loaded)
                if case.get("status") == "passed" and (
                    target_was_loaded != definition["expected_activation"]
                ):
                    errors.append(f"evaluation case {case_id!r} records a false activation for {target!r}")
                activation_passed = run.get("activation_passed")
                if not isinstance(activation_passed, bool):
                    errors.append(f"evaluation case {case_id!r} must record repeat-level activation evidence for {target!r}")
                elif activation_passed is not (target_was_loaded == definition["expected_activation"]):
                    errors.append(f"evaluation case {case_id!r} has inconsistent repeat-level activation evidence for {target!r}")
                if run.get("judge_status") != "completed":
                    errors.append(f"evaluation case {case_id!r} has incomplete aggregate judge status for {target!r}")
                treatment_scores = run.get("treatment_scores")
                criteria_count = len(definition["success_criteria"])
                if not isinstance(treatment_scores, list) or len(treatment_scores) != criteria_count or not all(type(item) is bool for item in treatment_scores):
                    errors.append(f"evaluation case {case_id!r} must record every treatment criterion score for {target!r}")
                    treatment_scores = []
                baseline_scores = run.get("baseline_scores")
                judge_votes = run.get("judge_votes")
                if not isinstance(judge_votes, list) or len(judge_votes) != RUBRIC_JUDGE_VOTES:
                    errors.append(
                        f"evaluation case {case_id!r} needs {RUBRIC_JUDGE_VOTES} rubric judge votes per repeat for {target!r}"
                    )
                    judge_votes = []
                valid_votes: list[dict[str, Any]] = []
                for vote in judge_votes:
                    if not isinstance(vote, dict) or vote.get("judge_status") != "completed":
                        errors.append(f"evaluation case {case_id!r} has incomplete rubric judge votes for {target!r}")
                        continue
                    vote_treatment = vote.get("treatment_scores")
                    vote_baseline = vote.get("baseline_scores")
                    vote_safety = vote.get("safety_regression")
                    if (not isinstance(vote_treatment, list) or len(vote_treatment) != criteria_count
                            or not all(type(item) is bool for item in vote_treatment)):
                        errors.append(f"evaluation case {case_id!r} has invalid treatment rubric votes for {target!r}")
                        continue
                    if definition["kind"] == "task":
                        if (not isinstance(vote_baseline, list) or len(vote_baseline) != criteria_count
                                or not all(type(item) is bool for item in vote_baseline)):
                            errors.append(f"task case {case_id!r} has invalid baseline rubric votes for {target!r}")
                            continue
                    elif vote_baseline is not None:
                        errors.append(f"trigger case {case_id!r} has unexpected baseline rubric votes for {target!r}")
                        continue
                    if type(vote_safety) is not bool:
                        errors.append(f"evaluation case {case_id!r} has invalid safety judge votes for {target!r}")
                        continue
                    valid_votes.append(vote)
                if len(valid_votes) == RUBRIC_JUDGE_VOTES:
                    majority = RUBRIC_JUDGE_VOTES // 2 + 1
                    expected_treatment = [
                        sum(vote["treatment_scores"][index] for vote in valid_votes) >= majority
                        for index in range(criteria_count)
                    ]
                    if treatment_scores != expected_treatment:
                        errors.append(f"evaluation case {case_id!r} treatment scores do not match judge majority for {target!r}")
                    expected_safety = any(vote["safety_regression"] for vote in valid_votes)
                    if run.get("safety_regression") is not expected_safety:
                        errors.append(f"evaluation case {case_id!r} safety result does not conservatively aggregate judge votes for {target!r}")
                    if definition["kind"] == "task" and all(
                        isinstance(vote.get("baseline_scores"), list)
                        and len(vote["baseline_scores"]) == criteria_count
                        and all(type(item) is bool for item in vote["baseline_scores"])
                        for vote in valid_votes
                    ):
                        expected_baseline = [
                            sum(vote["baseline_scores"][index] for vote in valid_votes) >= majority
                            for index in range(criteria_count)
                        ]
                        if baseline_scores != expected_baseline:
                            errors.append(f"task case {case_id!r} baseline scores do not match judge majority for {target!r}")
                effective_treatment_scores = treatment_scores
                effective_baseline_scores = baseline_scores
                if "human_adjudication" in run:
                    (
                        effective_treatment_scores,
                        effective_baseline_scores,
                        adjudication_errors,
                    ) = validate_human_adjudication(
                        run["human_adjudication"],
                        treatment_scores,
                        baseline_scores,
                        criteria_count,
                        definition["kind"] == "task",
                        case_id,
                        target,
                    )
                    errors.extend(adjudication_errors)
                effective_scores_by_repeat[repeat_number] = effective_treatment_scores
                baseline_status = run.get("baseline_status")
                baseline_ids = run.get("baseline_loaded_skill_ids")
                baseline_scores = run.get("baseline_scores")
                if definition["kind"] == "task":
                    if baseline_status != "completed":
                        errors.append(f"task case {case_id!r} has missing baseline evidence for {target!r}")
                    if not isinstance(baseline_ids, list) or not all(isinstance(item, str) for item in baseline_ids):
                        errors.append(f"task case {case_id!r} must record repeat-level baseline skill IDs for {target!r}")
                        baseline_ids = []
                    observed_baseline.update(baseline_ids)
                    if not isinstance(baseline_scores, list) or len(baseline_scores) != criteria_count or not all(type(item) is bool for item in baseline_scores):
                        errors.append(f"task case {case_id!r} must record every baseline criterion score for {target!r}")
                        baseline_scores = []
                    elif case.get("status") == "passed":
                        policy = definition["comparison_policy"]
                        treatment_score = sum(effective_treatment_scores)
                        baseline_score = sum(effective_baseline_scores or [])
                        if (not all(effective_treatment_scores)
                                or (policy == "uplift" and treatment_score <= baseline_score)
                                or (policy == "no-regression" and treatment_score < baseline_score)):
                            errors.append(f"task case {case_id!r} does not satisfy its rubric comparison for {target!r}")
                elif baseline_status is not None or baseline_ids is not None or baseline_scores is not None:
                    errors.append(f"trigger case {case_id!r} must not claim baseline results for {target!r}")
                safety_regression = run.get("safety_regression")
                if not isinstance(safety_regression, bool):
                    errors.append(f"evaluation case {case_id!r} must record repeat-level safety evidence for {target!r}")
                elif safety_regression:
                    safety_observed = True
                    errors.append(f"evaluation case {case_id!r} records a safety regression for {target!r}")
            if sorted(observed_loaded) != sorted(loaded_skills):
                errors.append(f"evaluation case {case_id!r} loaded skill summary does not match repeat evidence for {target!r}")
            if runs_with_target != target_runs:
                errors.append(f"evaluation case {case_id!r} target-skill count does not match repeat evidence for {target!r}")
            if case.get("status") == "passed":
                for run in run_evidence:
                    if not isinstance(run, dict):
                        continue
                    effective_scores = effective_scores_by_repeat.get(
                        run.get("repeat"), run.get("treatment_scores")
                    )
                    if (run.get("activation_passed") is not True
                            or not isinstance(effective_scores, list) or not all(effective_scores)):
                        errors.append(f"evaluation case {case_id!r} has a failed repeat in a passing result for {target!r}")
                        break
            safety_regression = case.get("safety_regression")
            if not isinstance(safety_regression, bool):
                errors.append(f"evaluation case {case_id!r} must record safety_regression for {target!r}")
            elif safety_regression or safety_observed:
                errors.append(f"evaluation case {case_id!r} records a safety regression for {target!r}")
            if case.get("status") == "failed" and not definition["critical"]:
                rationale = case.get("rationale")
                if not isinstance(rationale, str) or not rationale.strip():
                    errors.append(f"non-critical failure {case_id!r} needs a rationale for {target!r}")
            if definition["kind"] == "task":
                baseline_repeats = case.get("baseline_repeats")
                if not isinstance(baseline_repeats, int) or isinstance(baseline_repeats, bool) or baseline_repeats < definition["repeats"]:
                    errors.append(f"task case {case_id!r} needs enough baseline repeats for {target!r}")
                elif baseline_repeats != repeats:
                    errors.append(f"task case {case_id!r} baseline repeats must match paired treatment repeats for {target!r}")
                baseline_loaded_skills = case.get("baseline_loaded_skill_ids")
                if not isinstance(baseline_loaded_skills, list) or not all(isinstance(item, str) for item in baseline_loaded_skills):
                    errors.append(f"task case {case_id!r} must list baseline-loaded skill IDs for {target!r}")
                elif sorted(observed_baseline) != sorted(baseline_loaded_skills):
                    errors.append(f"task case {case_id!r} baseline skill summary does not match repeat evidence for {target!r}")
            if definition["critical"] and case.get("status") != "passed":
                errors.append(f"critical evaluation case failed for {target!r}: {case_id}")
    return errors


def safe_files(set_root: Path, relative_path: str):
    root = (set_root / relative_path).resolve()
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"skill archives do not support symlinked files: {path.relative_to(ROOT)}")
        if not path.is_file() or "evals" in path.relative_to(root).parts:
            continue
        yield path, Path(relative_path) / path.relative_to(root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("set_name", help="name of the set under sets/")
    parser.add_argument("--output", type=Path, default=Path("dist"), help="output directory")
    parser.add_argument("--for-release", action="store_true", help="require complete passing evidence")
    parser.add_argument("--tag", help="release tag; checked against the set name and version")
    args = parser.parse_args()

    errors, _ = validate_repo(require_validator=False)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    set_root = ROOT / "sets" / args.set_name
    descriptor_path = set_root / "set.json"
    if not descriptor_path.is_file():
        print(f"Unknown set: {args.set_name}", file=sys.stderr)
        return 2
    descriptor = json.loads(descriptor_path.read_text(encoding="utf-8"))
    version = descriptor["version"]
    targets = descriptor["target_runtimes"]
    if args.tag and args.tag != f"{args.set_name}/v{version}":
        print(f"tag must be {args.set_name}/v{version}", file=sys.stderr)
        return 1

    report_path = set_root / "reports" / f"{version}.json"
    if args.for_release:
        if descriptor.get("evaluation_status") != "passed":
            print("set.json evaluation_status must be 'passed' for release", file=sys.stderr)
            return 1
        if set(descriptor.get("tested_runtimes", [])) != set(targets):
            print("set.json must list every target runtime as tested for a release", file=sys.stderr)
            return 1
        report_errors = validate_report(report_path, args.set_name, version, targets)
        if report_errors:
            for error in report_errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1

    output_dir = args.output if args.output.is_absolute() else ROOT / args.output
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{args.set_name}-{version}.zip"
    set_license = set_root / "LICENSE"
    if set_license.is_file():
        license_path = set_license
    elif descriptor["license"] == "Apache-2.0":
        license_path = ROOT / "LICENSE"
    else:
        print(f"missing license file for {descriptor['license']}", file=sys.stderr)
        return 1
    try:
        package_files = [
            item
            for member in descriptor["skills"]
            for item in safe_files(set_root, member["path"])
        ]
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        prefix = Path(args.set_name)
        for top_level in ("set.json", "README.md"):
            bundle.write(set_root / top_level, prefix / top_level)
        bundle.write(license_path, prefix / "LICENSE")
        for source, relative in package_files:
            bundle.write(source, prefix / relative)

    print(f"Built {archive.relative_to(ROOT)} at {datetime.now(timezone.utc).isoformat()}")
    if args.for_release:
        report_copy = output_dir / "evaluation-report.json"
        report_copy.write_bytes(report_path.read_bytes())
        print(f"Attached report source: {report_copy.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
