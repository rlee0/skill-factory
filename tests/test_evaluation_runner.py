from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.run_evaluations import configure_workspace, loaded_skill_ids


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


if __name__ == "__main__":
    unittest.main()
