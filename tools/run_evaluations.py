#!/usr/bin/env python3
"""Run one skill set's cases in a restricted OpenCode workspace."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from .check_repo import ROOT, validate_repo
except ImportError:  # Direct script execution.
    from check_repo import ROOT, validate_repo

API_KEY_ENV = "OPENCODE_API_KEY"


def load_set(set_name: str) -> tuple[dict[str, Any], Path]:
    set_root = ROOT / "sets" / set_name
    descriptor_path = set_root / "set.json"
    if not descriptor_path.is_file():
        raise ValueError(f"unknown set: {set_name}")
    return json.loads(descriptor_path.read_text(encoding="utf-8")), set_root


def runtime_version(binary: str, env: dict[str, str]) -> str:
    result = subprocess.run([binary, "--version"], capture_output=True, text=True, env=env, check=False)
    if result.returncode:
        raise RuntimeError(f"could not read runtime version for {binary}: {result.stderr.strip()}")
    return (result.stdout or result.stderr).strip().splitlines()[0]


def install_skills(workspace: Path, set_root: Path, members: list[dict[str, str]]) -> None:
    target_root = workspace / ".agents/skills"
    target_root.mkdir(parents=True, exist_ok=True)
    for member in members:
        shutil.copytree(set_root / member["path"], target_root / member["name"],
                        ignore=shutil.ignore_patterns("evals", "__pycache__", ".DS_Store"))


def configure_workspace(workspace: Path) -> None:
    # OpenCode V2 calls its command tool "shell". Deny every action by default
    # so new tools, shell, execute/Code Mode, and MCP tools stay unavailable.
    # Keep skill loading consistent across treatment and runtime-baseline runs.
    deny_all = {"action": "*", "resource": "*", "effect": "deny"}
    agent_permissions = [deny_all, {"action": "skill", "resource": "*", "effect": "allow"}]
    config = {
        "$schema": "https://opencode.ai/config.json",
        "default_agent": "skill-eval",
        "permissions": [deny_all],
        "agents": {
            "skill-eval": {
                "description": "Runs evaluation prompts with only the explicitly allowed skills.",
                "mode": "primary",
                "permissions": agent_permissions,
            }
        },
    }
    (workspace / "opencode.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")


def command_for(model: str, prompt: str, binary: str) -> list[str]:
    return [binary, "--standalone", "run", "--agent", "skill-eval", "--format", "json", "--model", model, prompt]


def loaded_skill_ids(stdout: str) -> list[str]:
    skill_ids: list[str] = []
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        part = event.get("part", {})
        if event.get("type") == "tool_use" and part.get("tool") == "skill":
            skill_id = part.get("state", {}).get("input", {}).get("id")
            if isinstance(skill_id, str):
                skill_ids.append(skill_id)
    return skill_ids


def read_api_key(dotenv_path: Path, environ: dict[str, str]) -> str | None:
    """Read OPENCODE_API_KEY from the shell environment or the ignored .env file."""
    if environ.get(API_KEY_ENV):
        return environ[API_KEY_ENV]
    if not dotenv_path.is_file():
        return None

    value: str | None = None
    for line_number, raw_line in enumerate(dotenv_path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].lstrip()
        key, separator, raw_value = line.partition("=")
        if key.strip() != API_KEY_ENV:
            continue
        if not separator:
            raise ValueError(f"{dotenv_path.name}:{line_number}: expected {API_KEY_ENV}=...")
        if value is not None:
            raise ValueError(f"{dotenv_path.name}:{line_number}: duplicate {API_KEY_ENV} entry")
        try:
            parts = shlex.split(raw_value, comments=True, posix=True)
        except ValueError as error:
            raise ValueError(f"{dotenv_path.name}:{line_number}: invalid {API_KEY_ENV} value") from error
        if len(parts) > 1:
            raise ValueError(f"{dotenv_path.name}:{line_number}: {API_KEY_ENV} must be one value")
        value = parts[0] if parts else ""
    return value or None


def minimal_environment(home: Path) -> dict[str, str]:
    keep = ("PATH", "TMPDIR", "TMP", "TEMP", "LANG", "LC_ALL", "SYSTEMROOT")
    env = {key: os.environ[key] for key in keep if key in os.environ}
    env["HOME"] = str(home)
    env["XDG_CONFIG_HOME"] = str(home / ".config")
    credential = read_api_key(ROOT / ".env", os.environ)
    if not credential:
        raise ValueError(f"required credential environment variable is unset: {API_KEY_ENV}")
    env[API_KEY_ENV] = credential
    return env


def run_once(
    binary: str,
    model: str,
    prompt: str,
    install_skill_set: bool,
    set_root: Path,
    members: list[dict[str, str]],
    timeout: int,
    output_dir: Path,
    run_id: str,
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="skill-eval-") as temp:
        workspace = Path(temp) / "workspace"
        home = Path(temp) / "home"
        workspace.mkdir()
        home.mkdir()
        if install_skill_set:
            install_skills(workspace, set_root, members)
        configure_workspace(workspace)
        env = minimal_environment(home)
        command = command_for(model, prompt, binary)
        started = time.monotonic()
        try:
            result = subprocess.run(
                command,
                cwd=workspace,
                env=env,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
            status = "completed" if result.returncode == 0 else "runtime-error"
            stdout = result.stdout
            stderr = result.stderr
            return_code = result.returncode
        except subprocess.TimeoutExpired as error:
            status = "timeout"
            stdout = error.stdout.decode("utf-8", errors="replace") if isinstance(error.stdout, bytes) else error.stdout or ""
            stderr = error.stderr.decode("utf-8", errors="replace") if isinstance(error.stderr, bytes) else error.stderr or ""
            return_code = None

    (output_dir / f"{run_id}.stdout").write_text(stdout, encoding="utf-8")
    (output_dir / f"{run_id}.stderr").write_text(stderr, encoding="utf-8")
    return {
        "id": run_id,
        "mode": "with-skill" if install_skill_set else "baseline",
        "status": status,
        "return_code": return_code,
        "duration_seconds": round(time.monotonic() - started, 2),
        "loaded_skills": loaded_skill_ids(stdout),
        "stdout_file": f"{run_id}.stdout",
        "stderr_file": f"{run_id}.stderr",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("set_name", help="name of the set under sets/")
    parser.add_argument("--model", required=True, help="exact runtime model identifier")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--smoke", action="store_true", help="run critical cases once each")
    selection.add_argument("--case", action="append", dest="case_ids", help="run only this case; may be repeated")
    parser.add_argument("--timeout", type=int, default=600, help="seconds allowed for each run")
    parser.add_argument("--output", type=Path, default=Path("evaluation-runs"))
    args = parser.parse_args()

    try:
        validation_errors, _ = validate_repo()
        if validation_errors:
            raise ValueError("repository checks must pass before evaluation: " + "; ".join(validation_errors))
        descriptor, set_root = load_set(args.set_name)
        binary = shutil.which("opencode")
        if not binary:
            raise ValueError("OpenCode CLI is not installed")
        if args.timeout < 1:
            raise ValueError("--timeout must be positive")

        all_cases: list[tuple[str, dict[str, Any]]] = []
        for member in descriptor["skills"]:
            cases_path = set_root / member["path"] / "evals" / "cases.json"
            cases_doc = json.loads(cases_path.read_text(encoding="utf-8"))
            all_cases.extend((member["name"], case) for case in cases_doc["cases"])
        if args.smoke:
            all_cases = [(skill, case) for skill, case in all_cases if case["critical"]]
        if args.case_ids:
            requested = set(args.case_ids)
            all_cases = [(skill, case) for skill, case in all_cases if case["id"] in requested]
            found = {case["id"] for _, case in all_cases}
            missing = requested - found
            if missing:
                raise ValueError(f"unknown case id(s): {', '.join(sorted(missing))}")
        if not all_cases:
            raise ValueError("no evaluation cases selected")

        output_root = args.output if args.output.is_absolute() else ROOT / args.output
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        run_dir = output_root / args.set_name / f"{timestamp}-opencode"
        run_dir.mkdir(parents=True, exist_ok=False)
        home = Path(tempfile.mkdtemp(prefix="skill-eval-version-"))
        try:
            env = minimal_environment(home)
            version = runtime_version(binary, env)
        finally:
            shutil.rmtree(home)

        runs: list[dict[str, Any]] = []
        for skill_name, case in all_cases:
            modes = (True,) if case["kind"] == "trigger" else (True, False)
            repeat_count = 1 if args.smoke else case["repeats"]
            for repeat in range(1, repeat_count + 1):
                for with_skill in modes:
                    run_id = f"{skill_name}-{case['id']}-r{repeat}-{'skill' if with_skill else 'baseline'}"
                    result = run_once(
                        binary,
                        args.model,
                        case["prompt"],
                        with_skill,
                        set_root,
                        descriptor["skills"],
                        args.timeout,
                        run_dir,
                        run_id,
                    )
                    runs.append({
                        "skill": skill_name,
                        "case": case["id"],
                        "kind": case["kind"],
                        "repeat": repeat,
                        "set_skills_installed": [member["name"] for member in descriptor["skills"]] if with_skill else [],
                        "expected_activation": case["expected_activation"],
                        "critical": case["critical"],
                        "success_criteria": case["success_criteria"],
                        **result,
                    })
                    print(f"{case['id']} {run_id}: {result['status']}")

        manifest = {
            "set": args.set_name,
            "set_version": descriptor["version"],
            "runtime": "OpenCode",
            "runtime_id": "opencode",
            "runtime_version": version,
            "model": args.model,
            "status": "pending-human-review",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "runs": runs,
            "review_note": "Inspect paired outputs against each case's success_criteria; this runner does not score model responses.",
        }
        (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        failed_runs = sum(run["status"] != "completed" for run in runs)
        try:
            display_dir = run_dir.relative_to(ROOT)
        except ValueError:
            display_dir = run_dir
        print(f"Saved review artifacts to {display_dir}")
        if failed_runs:
            print(f"{failed_runs} run(s) failed or timed out; this evidence cannot pass release review.", file=sys.stderr)
            return 1
        print("Runs completed; human rubric review is still required before recording a passing report.")
        return 0
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
