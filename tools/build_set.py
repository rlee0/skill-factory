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
except ImportError:  # Direct script execution.
    from check_repo import ROOT, read_json, validate_repo


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
            elif case.get("status") == "passed":
                expected_runs_with_target = repeats if definition["expected_activation"] else 0
                if runs_with_target != expected_runs_with_target:
                    errors.append(f"evaluation case {case_id!r} has the wrong target-skill activation count for {target!r}")
                if definition["expected_activation"] and target_skill not in loaded_skills:
                    errors.append(f"evaluation case {case_id!r} did not record its target skill as loaded for {target!r}")
                if not definition["expected_activation"] and target_skill in loaded_skills:
                    errors.append(f"evaluation case {case_id!r} records a false activation for {target!r}")
            safety_regression = case.get("safety_regression")
            if not isinstance(safety_regression, bool):
                errors.append(f"evaluation case {case_id!r} must record safety_regression for {target!r}")
            elif safety_regression:
                errors.append(f"evaluation case {case_id!r} records a safety regression for {target!r}")
            if case.get("status") == "failed" and not definition["critical"]:
                rationale = case.get("rationale")
                if not isinstance(rationale, str) or not rationale.strip():
                    errors.append(f"non-critical failure {case_id!r} needs a rationale for {target!r}")
            if definition["kind"] == "task":
                baseline_repeats = case.get("baseline_repeats")
                if not isinstance(baseline_repeats, int) or isinstance(baseline_repeats, bool) or baseline_repeats < definition["repeats"]:
                    errors.append(f"task case {case_id!r} needs enough baseline repeats for {target!r}")
                baseline_loaded_skills = case.get("baseline_loaded_skill_ids")
                if not isinstance(baseline_loaded_skills, list) or not all(isinstance(item, str) for item in baseline_loaded_skills):
                    errors.append(f"task case {case_id!r} must list baseline-loaded skill IDs for {target!r}")
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
