from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.run_evaluations import (
    affected_skills,
    assistant_text,
    ci_passes,
    configure_workspace,
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

    def test_judgment_requires_exact_boolean_arrays(self) -> None:
        output = json.dumps({"type": "text", "part": {"text": '{"treatment":[true,false],"baseline":[false,true]}'}})
        self.assertEqual(([True, False], [False, True]), parse_judgment(output, 2, True))
        invalid = json.dumps({"type": "text", "part": {"text": '{"treatment":[1],"baseline":null}'}})
        with self.assertRaisesRegex(ValueError, "invalid result"):
            parse_judgment(invalid, 1, False)

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
        }
        self.assertTrue(ci_passes([base]))
        self.assertFalse(ci_passes([{**base, "status": "failed"}]))
        self.assertFalse(ci_passes([{**base, "activation_errors": 1}]))
        self.assertFalse(ci_passes([{**base, "runtime_errors": 1}]))
        self.assertTrue(ci_passes([{**base, "critical": False, "status": "failed"}]))


if __name__ == "__main__":
    unittest.main()
