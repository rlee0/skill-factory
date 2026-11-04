from __future__ import annotations

import json
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from tools.run_evaluations import (
    affected_skills,
    assistant_text,
    ci_passes,
    configure_workspace,
    evaluate_case,
    has_runtime_evidence,
    loaded_skill_ids,
    parse_judgment,
)


class ConfigureWorkspaceTests(unittest.TestCase):
    def test_only_skill_loading_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            configure_workspace(workspace)
            config = json.loads((workspace / "opencode.json").read_text(encoding="utf-8"))

        self.assertEqual("skill-eval", config["default_agent"])
        self.assertEqual("primary", config["agents"]["skill-eval"]["mode"])
        self.assertEqual(
            [{"action": "*", "resource": "*", "effect": "deny"}],
            config["agents"]["rubric-judge"]["permissions"],
        )
        self.assertEqual(
            [{"action": "*", "resource": "*", "effect": "deny"}],
            config["permissions"],
        )
        self.assertEqual(
            [
                {"action": "*", "resource": "*", "effect": "deny"},
                {"action": "skill", "resource": "*", "effect": "allow"},
            ],
            config["agents"]["skill-eval"]["permissions"],
        )

    def test_loaded_skill_ids_are_extracted_from_jsonl(self) -> None:
        output = '\n'.join([
            json.dumps({"type": "tool_use", "part": {"tool": "skill", "state": {"input": {"id": "author-skills"}}}}),
            json.dumps({"type": "tool_use", "part": {"tool": "shell", "state": {"input": {"command": "ls"}}}}),
        ])
        self.assertEqual(["author-skills"], loaded_skill_ids(output))

    def test_assistant_text_is_extracted_from_jsonl(self) -> None:
        output = json.dumps({"type": "text", "part": {"type": "text", "text": '{"treatment":[true],"baseline":null}'}})
        self.assertEqual('{"treatment":[true],"baseline":null}', assistant_text(output))
        self.assertTrue(has_runtime_evidence(output))
        self.assertFalse(has_runtime_evidence(""))
        self.assertFalse(has_runtime_evidence('{"type":"step-finish"}'))

    def test_judgment_requires_exact_boolean_arrays(self) -> None:
        output = json.dumps({"type": "text", "part": {"text": '{"treatment":[true,false],"baseline":[false,true],"safety_regression":false}'}})
        self.assertEqual(([True, False], [False, True], False), parse_judgment(output, 2, True))
        invalid = json.dumps({"type": "text", "part": {"text": '{"treatment":[1],"baseline":null,"safety_regression":false}'}})
        with self.assertRaisesRegex(ValueError, "invalid result"):
            parse_judgment(invalid, 1, False)

    def test_evaluation_retains_each_treatment_and_native_baseline_skill_observation(self) -> None:
        case = {
            "id": "task-case",
            "kind": "task",
            "prompt": "Do the task",
            "expected_activation": True,
            "critical": True,
            "repeats": 2,
            "comparison_policy": "no-regression",
            "success_criteria": ["criterion"],
        }
        completed = {"status": "completed", "evidence_observed": True, "loaded_skills": ["target"], "stdout": "answer"}
        baseline = {**completed, "loaded_skills": ["native-skill"]}
        judgment = {"status": "completed", "evidence_observed": True, "loaded_skills": [],
                    "stdout": json.dumps({"type": "text", "part": {"text": '{"treatment":[true],"baseline":[true],"safety_regression":false}'}})}
        with patch("tools.run_evaluations.execute_once", side_effect=[completed, baseline, judgment] * 2):
            result = evaluate_case("opencode", "model-id", "target", case, Path("set"), [], 1, Path("source"))
        self.assertEqual("passed", result["status"])
        self.assertEqual(["target"], result["loaded_skill_ids"])
        self.assertEqual(["native-skill"], result["baseline_loaded_skill_ids"])
        self.assertEqual(2, result["baseline_repeats"])
        self.assertEqual(["target"], result["run_evidence"][0]["treatment_loaded_skill_ids"])
        self.assertEqual(["native-skill"], result["run_evidence"][0]["baseline_loaded_skill_ids"])

    def test_missing_runtime_evidence_fails_instead_of_counting_as_no_activation(self) -> None:
        case = {
            "id": "trigger-case",
            "kind": "trigger",
            "prompt": "Evaluate behavior",
            "expected_activation": False,
            "critical": False,
            "repeats": 1,
            "success_criteria": ["criterion"],
        }
        missing = {"status": "completed", "evidence_observed": False, "loaded_skills": [], "stdout": ""}
        with patch("tools.run_evaluations.execute_once", return_value=missing):
            result = evaluate_case("opencode", "model-id", "target", case, Path("set"), [], 1, Path("source"))
        self.assertEqual("failed", result["status"])
        self.assertEqual(1, result["runtime_errors"])
        self.assertEqual("missing", result["run_evidence"][0]["treatment_status"])

    def test_failed_runs_preserve_evidence_shape_and_path_specific_status(self) -> None:
        case = {
            "id": "task-case",
            "kind": "task",
            "prompt": "Do the task",
            "expected_activation": True,
            "critical": True,
            "repeats": 1,
            "comparison_policy": "no-regression",
            "success_criteria": ["criterion"],
        }
        treatment = {
            "status": "completed",
            "evidence_observed": True,
            "loaded_skills": ["target"],
            "stdout": "answer",
        }
        baseline = {
            "status": "completed",
            "evidence_observed": True,
            "loaded_skills": ["native-skill"],
            "stdout": "baseline answer",
        }
        failed_paths = [
            (
                [
                    {**treatment, "status": "runtime-error", "evidence_observed": False},
                    baseline,
                ],
                "runtime-error",
                None,
            ),
            (
                [treatment, baseline, {"status": "runtime-error", "evidence_observed": False}],
                "completed",
                "runtime-error",
            ),
            (
                [
                    treatment,
                    baseline,
                    {
                        "status": "completed",
                        "evidence_observed": True,
                        "loaded_skills": [],
                        "stdout": json.dumps({"type": "text", "part": {"text": "not json"}}),
                    },
                ],
                "completed",
                "invalid-result",
            ),
        ]
        expected_fields = {
            "repeat",
            "treatment_status",
            "treatment_loaded_skill_ids",
            "activation_passed",
            "treatment_scores",
            "baseline_status",
            "baseline_loaded_skill_ids",
            "baseline_scores",
            "judge_status",
            "safety_regression",
        }

        for responses, treatment_status, judge_status in failed_paths:
            with self.subTest(treatment_status=treatment_status, judge_status=judge_status):
                with patch("tools.run_evaluations.execute_once", side_effect=responses):
                    result = evaluate_case(
                        "opencode", "model-id", "target", case, Path("set"), [], 1, Path("source")
                    )

                evidence = result["run_evidence"][0]
                self.assertEqual("failed", result["status"])
                self.assertEqual(1, result["runtime_errors"])
                self.assertEqual(expected_fields, set(evidence))
                self.assertEqual(treatment_status, evidence["treatment_status"])
                self.assertEqual(judge_status, evidence["judge_status"])
                self.assertEqual(["target"], evidence["treatment_loaded_skill_ids"])
                self.assertEqual(["native-skill"], evidence["baseline_loaded_skill_ids"])
                self.assertEqual("completed", evidence["baseline_status"])
                self.assertIsNone(evidence["treatment_scores"])
                self.assertIsNone(evidence["baseline_scores"])

    def test_changed_skill_files_select_only_their_member(self) -> None:
        descriptor = {"skills": [
            {"name": "alpha", "path": "skills/alpha"},
            {"name": "beta", "path": "skills/beta"},
        ]}
        self.assertEqual(
            {"beta"},
            affected_skills("sample", descriptor, {"sets/sample/skills/beta/references/guide.md"}),
        )
        self.assertEqual(
            {"alpha", "beta"},
            affected_skills("sample", descriptor, {"sets/sample/set.json"}),
        )
        self.assertEqual(set(), affected_skills("sample", descriptor, {"sets/sample/README.md"}))

    def test_ci_blocks_critical_rubric_runtime_and_activation_failures(self) -> None:
        base = {
            "critical": True,
            "status": "passed",
            "activation_errors": 0,
            "runtime_errors": 0,
            "safety_regression": False,
            "skill": "target",
            "kind": "trigger",
            "expected_activation": True,
            "repeats": 1,
            "loaded_skill_ids": ["target"],
            "runs_with_target_skill": 1,
            "run_evidence": [{
                "treatment_status": "completed",
                "treatment_loaded_skill_ids": ["target"],
                "activation_passed": True,
                "treatment_scores": [True],
                "judge_status": "completed",
                "safety_regression": False,
            }],
        }
        self.assertTrue(ci_passes([base]))
        self.assertFalse(ci_passes([{**base, "status": "failed"}]))
        self.assertFalse(ci_passes([{**base, "activation_errors": 1}]))
        self.assertFalse(ci_passes([{**base, "runtime_errors": 1}]))
        self.assertTrue(ci_passes([{**base, "critical": False, "status": "failed"}]))
        self.assertFalse(ci_passes([{**base, "critical": False, "safety_regression": True}]))
        self.assertFalse(ci_passes([{key: value for key, value in base.items() if key != "run_evidence"}]))


if __name__ == "__main__":
    unittest.main()
