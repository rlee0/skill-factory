from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from tools.check_repo import validate_repo


class EvaluationEvidenceConsistencyTests(unittest.TestCase):
    def make_repo(
        self,
        *,
        evaluation_status: str = "passed",
        tested_runtimes: list[str] | None = None,
        report_version: str | None = "1.2.3",
        report_status: str = "passed",
        report_set: str = "example",
        report_data_version: str | None = None,
        report_runtimes: list[dict[str, str]] | None = None,
    ) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        set_root = root / "sets" / "example"
        skill_root = set_root / "skills" / "demo"
        (skill_root / "evals").mkdir(parents=True)
        (set_root / "reports").mkdir()

        descriptor: dict[str, Any] = {
            "schema_version": 1,
            "name": "example",
            "version": "1.2.3",
            "description": "A test skill set.",
            "license": "Apache-2.0",
            "skills": [{"name": "demo", "path": "skills/demo"}],
            "target_runtimes": ["OpenCode", "OtherRuntime"],
            "tested_runtimes": tested_runtimes if tested_runtimes is not None else ["OpenCode"],
            "evaluation_status": evaluation_status,
        }
        (set_root / "set.json").write_text(json.dumps(descriptor), encoding="utf-8")
        (skill_root / "SKILL.md").write_text(
            "---\nname: demo\ndescription: A demo skill.\n---\n\nInstructions.\n",
            encoding="utf-8",
        )
        cases = {
            "schema_version": 1,
            "skill": "demo",
            "baseline": "OpenCode without the candidate set.",
            "cases": [
                {
                    "id": "demo-trigger",
                    "kind": "trigger",
                    "prompt": "Use the demo skill.",
                    "expected_activation": True,
                    "critical": True,
                    "repeats": 1,
                    "success_criteria": ["The skill activates."],
                },
                {
                    "id": "demo-task",
                    "kind": "task",
                    "prompt": "Complete a demo task.",
                    "expected_activation": True,
                    "critical": True,
                    "repeats": 1,
                    "success_criteria": ["The task is completed."],
                    "comparison_policy": "uplift",
                },
            ],
        }
        (skill_root / "evals" / "cases.json").write_text(json.dumps(cases), encoding="utf-8")

        if report_version is not None:
            report = {
                "set": report_set,
                "version": report_data_version if report_data_version is not None else report_version,
                "status": report_status,
                "runtimes": report_runtimes if report_runtimes is not None else [
                    {"name": "OpenCode", "status": "passed"}
                ],
            }
            report_path = set_root / "reports" / f"{report_version}.json"
            report_path.write_text(json.dumps(report), encoding="utf-8")
        return temporary, root

    def validate_fixture(self, **kwargs: Any) -> list[str]:
        temporary, root = self.make_repo(**kwargs)
        self.addCleanup(temporary.cleanup)
        errors, _ = validate_repo(root=root)
        return errors

    def test_passing_report_for_claimed_runtime_allows_other_targets_untested(self) -> None:
        errors = self.validate_fixture(
            tested_runtimes=["OpenCode"],
            report_runtimes=[{"name": "OpenCode", "status": "passed"}],
        )

        self.assertEqual([], errors)

    def test_passed_descriptor_requires_report_for_its_exact_version(self) -> None:
        errors = self.validate_fixture(report_version=None)

        self.assertTrue(any("1.2.3" in error and "report" in error for error in errors))

    def test_report_for_an_older_version_does_not_support_current_claims(self) -> None:
        errors = self.validate_fixture(report_version="1.2.2")

        self.assertTrue(any("1.2.3" in error and "report" in error for error in errors))

    def test_passing_descriptor_requires_report_for_same_set_and_version(self) -> None:
        errors = self.validate_fixture(report_set="other", report_data_version="1.2.2")

        self.assertTrue(any("report set does not match" in error for error in errors))
        self.assertTrue(any("report version does not match" in error for error in errors))

    def test_passing_descriptor_requires_overall_report_to_pass(self) -> None:
        errors = self.validate_fixture(report_status="failed")

        self.assertTrue(any("report status is not 'passed'" in error for error in errors))

    def test_each_claimed_tested_runtime_needs_a_passing_report_entry(self) -> None:
        errors = self.validate_fixture(
            tested_runtimes=["OpenCode", "OtherRuntime"],
            report_runtimes=[{"name": "OpenCode", "status": "passed"}],
        )

        self.assertTrue(any("OtherRuntime" in error and "report" in error for error in errors))

    def test_claimed_tested_runtime_must_have_a_passing_entry(self) -> None:
        errors = self.validate_fixture(
            report_runtimes=[{"name": "OpenCode", "status": "failed"}],
        )

        self.assertTrue(any("OpenCode" in error and "passing report result" in error for error in errors))

    def test_pending_set_may_have_no_report_or_tested_runtimes(self) -> None:
        errors = self.validate_fixture(
            evaluation_status="pending",
            tested_runtimes=[],
            report_version=None,
        )

        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
