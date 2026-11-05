from __future__ import annotations

import unittest
from typing import Any

from tools.evaluation_contract import AdjudicatedScores, RUBRIC_JUDGE_VOTES, assess_case


class AssessCaseTests(unittest.TestCase):
    def task_result(
        self,
        treatment_scores: list[bool],
        baseline_scores: list[bool],
        *,
        policy: str = "uplift",
        status: str = "passed",
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        definition = {
            "id": "task-one",
            "kind": "task",
            "critical": True,
            "expected_activation": True,
            "repeats": 1,
            "comparison_policy": policy,
            "success_criteria": ["first criterion", "second criterion"],
            "skill": "target",
        }
        votes = [
            {
                "judge_status": "completed",
                "treatment_scores": treatment_scores,
                "baseline_scores": baseline_scores,
                "safety_regression": False,
            }
            for _ in range(RUBRIC_JUDGE_VOTES)
        ]
        treatment_passed = all(treatment_scores) and (
            sum(treatment_scores) > sum(baseline_scores)
            if policy == "uplift"
            else sum(treatment_scores) >= sum(baseline_scores)
        )
        result = {
            "skill": "target",
            "case": "task-one",
            "kind": "task",
            "critical": True,
            "expected_activation": True,
            "repeats": 1,
            "status": status,
            "activation_errors": 0,
            "runtime_errors": 0,
            "rubric_failures": int(not treatment_passed),
            "runs_with_target_skill": 1,
            "loaded_skill_ids": ["target"],
            "safety_regression": False,
            "baseline_repeats": 1,
            "baseline_loaded_skill_ids": [],
            "baseline_passes": int(all(baseline_scores)),
            "run_evidence": [{
                "repeat": 1,
                "treatment_status": "completed",
                "treatment_loaded_skill_ids": ["target"],
                "activation_passed": True,
                "treatment_scores": treatment_scores,
                "treatment_passed": treatment_passed,
                "baseline_status": "completed",
                "baseline_loaded_skill_ids": [],
                "baseline_scores": baseline_scores,
                "baseline_passed": all(baseline_scores),
                "judge_status": "completed",
                "judge_votes": votes,
                "safety_regression": False,
            }],
        }
        return definition, result

    def test_uplift_requires_a_strictly_greater_treatment_count(self) -> None:
        definition, result = self.task_result([True, True], [True, True], status="passed")

        assessed, errors = assess_case(definition, result)

        self.assertEqual("failed", assessed["status"])
        self.assertTrue(any("failed repeat in a passing result" in error for error in errors))

    def test_no_regression_accepts_equal_counts_when_treatment_passes_all_criteria(self) -> None:
        definition, result = self.task_result(
            [True, True], [True, True], policy="no-regression", status="passed"
        )

        assessed, errors = assess_case(definition, result)

        self.assertEqual("passed", assessed["status"])
        self.assertEqual([], errors)

    def test_validated_human_scores_affect_outcome_not_automated_evidence(self) -> None:
        definition, result = self.task_result([False, True], [True, False], status="passed")

        assessed, errors = assess_case(
            definition,
            result,
            adjudicated_scores_by_repeat={1: AdjudicatedScores([True, True], [True, False])},
        )

        self.assertEqual("passed", assessed["status"])
        self.assertEqual([False, True], assessed["run_evidence"][0]["treatment_scores"])
        self.assertEqual([], errors)

    def test_safety_vote_remains_blocking_when_its_rubric_scores_are_malformed(self) -> None:
        definition, result = self.task_result([True, True], [True, False], status="passed")
        result["run_evidence"][0]["judge_votes"][0]["treatment_scores"] = [True]
        result["run_evidence"][0]["judge_votes"][0]["safety_regression"] = True

        assessed, errors = assess_case(definition, result)

        self.assertTrue(assessed["safety_regression"])
        self.assertTrue(any("safety regression" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
