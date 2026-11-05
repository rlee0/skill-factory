from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from tools.build_set import validate_report
from tools.evaluation_contract import RUBRIC_JUDGE_VOTES


ROOT = Path(__file__).resolve().parents[1]
SET_ROOT = ROOT / "sets" / "skill-factory"


def evaluation_cases() -> list[tuple[str, dict[str, Any]]]:
    descriptor = json.loads((SET_ROOT / "set.json").read_text(encoding="utf-8"))
    cases: list[tuple[str, dict[str, Any]]] = []
    for member in descriptor["skills"]:
        path = SET_ROOT / member["path"] / "evals" / "cases.json"
        cases.extend((member["name"], case) for case in json.loads(path.read_text(encoding="utf-8"))["cases"])
    return cases


def report_document() -> dict[str, Any]:
    cases = evaluation_cases()
    runtimes = []
    for name in ("OpenCode",):
        runtime_cases = []
        for skill_name, case in cases:
            baseline_scores = [
                case["comparison_policy"] != "uplift"
                for _ in case["success_criteria"]
            ] if case["kind"] == "task" else None
            result = {
                "id": case["id"],
                "status": "passed",
                "critical": case["critical"],
                "safety_regression": False,
                "repeats": case["repeats"],
                "expected_activation": case["expected_activation"],
                "runs_with_target_skill": case["repeats"] if case["expected_activation"] else 0,
                "loaded_skill_ids": [skill_name] if case["expected_activation"] else [],
                "run_evidence": [
                    {
                        "repeat": repeat,
                        "treatment_status": "completed",
                        "treatment_loaded_skill_ids": [skill_name] if case["expected_activation"] else [],
                        "activation_passed": True,
                        "treatment_scores": [True] * len(case["success_criteria"]),
                        "baseline_status": "completed" if case["kind"] == "task" else None,
                        "baseline_loaded_skill_ids": [] if case["kind"] == "task" else None,
                        "baseline_scores": baseline_scores,
                        "judge_status": "completed",
                        "judge_votes": [
                            {
                                "judge_status": "completed",
                                "treatment_scores": [True] * len(case["success_criteria"]),
                                "baseline_scores": baseline_scores,
                                "safety_regression": False,
                            }
                            for _ in range(RUBRIC_JUDGE_VOTES)
                        ],
                        "safety_regression": False,
                    }
                    for repeat in range(1, case["repeats"] + 1)
                ],
            }
            if case["kind"] == "task":
                result["baseline_repeats"] = case["repeats"]
                result["baseline_loaded_skill_ids"] = []
            runtime_cases.append(result)
        runtimes.append({
            "name": name,
            "version": "test-runtime-1.0",
            "model": "test-model-1",
            "status": "passed",
            "cases": runtime_cases,
        })
    return {
        "set": "skill-factory",
        "version": "0.1.0",
        "status": "passed",
        "generated_at": "2026-01-01T00:00:00Z",
        "baseline_definition": "OpenCode without the candidate set; native OpenCode skills remain available.",
        "runtimes": runtimes,
    }


class ValidateReportTests(unittest.TestCase):
    def validate(self, document: dict[str, Any]) -> list[str]:
        with tempfile.TemporaryDirectory(dir=SET_ROOT / "reports") as temp_dir:
            path = Path(temp_dir) / "report.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            return validate_report(path, "skill-factory", "0.1.0", ["OpenCode"])

    def test_complete_passing_report_is_accepted(self) -> None:
        self.assertEqual([], self.validate(report_document()))

    def test_critical_failure_blocks_report(self) -> None:
        report = report_document()
        critical = next(case for case in report["runtimes"][0]["cases"] if case["critical"])
        critical["status"] = "failed"
        errors = self.validate(report)
        self.assertTrue(any("critical evaluation case failed" in error for error in errors))

    def test_missing_case_blocks_report(self) -> None:
        report = report_document()
        report["runtimes"][0]["cases"].pop()
        errors = self.validate(report)
        self.assertTrue(any("missing cases" in error for error in errors))

    def test_missing_task_baseline_blocks_report(self) -> None:
        report = report_document()
        task = next(case for case in report["runtimes"][0]["cases"] if case["id"] == "author-skill-usable-instructions")
        del task["baseline_repeats"]
        errors = self.validate(report)
        self.assertTrue(any("baseline repeats" in error for error in errors))

    def test_false_activation_blocks_a_passed_case(self) -> None:
        report = report_document()
        irrelevant = next(case for case in report["runtimes"][0]["cases"] if case["id"] == "release-set-unrelated-trigger")
        irrelevant["runs_with_target_skill"] = 1
        irrelevant["loaded_skill_ids"] = ["release-skill-set"]
        irrelevant["run_evidence"][0]["treatment_loaded_skill_ids"] = ["release-skill-set"]
        irrelevant["run_evidence"][0]["activation_passed"] = False
        errors = self.validate(report)
        self.assertTrue(any("false activation" in error for error in errors))

    def test_missing_repeat_evidence_blocks_a_passing_report(self) -> None:
        report = report_document()
        case = next(item for item in report["runtimes"][0]["cases"] if item["id"] == "release-set-unrelated-trigger")
        case["run_evidence"] = []
        errors = self.validate(report)
        self.assertTrue(any("repeat-level evidence" in error for error in errors))

    def test_missing_judge_votes_blocks_a_passing_report(self) -> None:
        report = report_document()
        case = next(item for item in report["runtimes"][0]["cases"] if item["id"] == "release-set-unrelated-trigger")
        case["run_evidence"][0]["judge_votes"] = []
        errors = self.validate(report)
        self.assertTrue(any("rubric judge votes" in error for error in errors))

    def test_aggregate_scores_must_match_recorded_judge_votes(self) -> None:
        report = report_document()
        case = next(item for item in report["runtimes"][0]["cases"] if item["id"] == "release-set-unrelated-trigger")
        for vote in case["run_evidence"][0]["judge_votes"][:2]:
            vote["treatment_scores"] = [False] * len(case["run_evidence"][0]["treatment_scores"])
        errors = self.validate(report)
        self.assertTrue(any("do not match judge majority" in error for error in errors))

    def test_any_safety_vote_blocks_even_when_it_is_not_the_majority(self) -> None:
        report = report_document()
        case = next(item for item in report["runtimes"][0]["cases"] if item["id"] == "release-set-unrelated-trigger")
        case["safety_regression"] = True
        run = case["run_evidence"][0]
        run["judge_votes"][0]["safety_regression"] = True
        run["safety_regression"] = True
        errors = self.validate(report)
        self.assertTrue(any("safety regression" in error for error in errors))

    def test_safety_regression_blocks_even_noncritical_case(self) -> None:
        report = report_document()
        case = next(item for item in report["runtimes"][0]["cases"] if item["id"] == "release-set-unrelated-trigger")
        case["safety_regression"] = True
        case["run_evidence"][0]["safety_regression"] = True
        errors = self.validate(report)
        self.assertTrue(any("safety regression" in error for error in errors))

    def test_runtime_and_model_identity_are_required(self) -> None:
        report = report_document()
        report["runtimes"][0]["version"] = ""
        report["runtimes"][0]["model"] = ""
        errors = self.validate(report)
        self.assertTrue(any("must record version" in error for error in errors))
        self.assertTrue(any("must record model" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
