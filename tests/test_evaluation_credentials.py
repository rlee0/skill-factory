from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.run_evaluations import API_KEY_ENV, read_api_key


class ReadApiKeyTests(unittest.TestCase):
    def read(self, contents: str, environ: dict[str, str] | None = None) -> str | None:
        with tempfile.TemporaryDirectory() as temp_dir:
            dotenv = Path(temp_dir) / ".env"
            dotenv.write_text(contents, encoding="utf-8")
            return read_api_key(dotenv, environ or {})

    def test_reads_key_from_env_file(self) -> None:
        self.assertEqual("test-key", self.read("OPENCODE_API_KEY=test-key\n"))

    def test_reads_quoted_key_and_ignores_comment(self) -> None:
        self.assertEqual("test-key", self.read('OPENCODE_API_KEY="test-key" # local credential\n'))

    def test_shell_environment_takes_precedence(self) -> None:
        self.assertEqual("shell-key", self.read("OPENCODE_API_KEY=file-key\n", {API_KEY_ENV: "shell-key"}))

    def test_ignores_other_keys(self) -> None:
        self.assertIsNone(self.read("OTHER_API_KEY=not-used\n"))

    def test_rejects_duplicate_key_entries(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate OPENCODE_API_KEY"):
            self.read("OPENCODE_API_KEY=first\nOPENCODE_API_KEY=second\n")


if __name__ == "__main__":
    unittest.main()
