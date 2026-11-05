#!/usr/bin/env python3
"""Validate set descriptors, evaluation cases, and Agent Skills directories."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def read_json(path: Path, errors: list[str], root: Path = ROOT) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{path.relative_to(root)}: cannot read JSON: {error}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(root)}: expected a JSON object")
        return None
    return value


def read_skill_name(skill_file: Path, errors: list[str], root: Path = ROOT) -> str | None:
    try:
        text = skill_file.read_text(encoding="utf-8")
    except OSError as error:
        errors.append(f"{skill_file.relative_to(root)}: cannot read: {error}")
        return None

    if not text.startswith("---\n"):
        errors.append(f"{skill_file.relative_to(root)}: YAML frontmatter must start on line 1")
        return None
    _, separator, _ = text[4:].partition("\n---\n")
    if not separator:
        errors.append(f"{skill_file.relative_to(root)}: missing closing frontmatter delimiter")
        return None

    header = text[4:].split("\n---\n", 1)[0]
    name_match = re.search(r"(?m)^name:\s*([^\s#]+)\s*$", header)
    description_match = re.search(r"(?m)^description:\s*(.+?)\s*$", header)
    if not name_match:
        errors.append(f"{skill_file.relative_to(root)}: missing scalar 'name' field")
        return None
    if not description_match:
        errors.append(f"{skill_file.relative_to(root)}: missing non-empty 'description' field")
    return name_match.group(1).strip("\"'")


def read_skill_license(skill_file: Path) -> str | None:
    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    header = text[4:].split("\n---\n", 1)[0]
    match = re.search(r"(?m)^license:\s*(.+?)\s*$", header)
    return match.group(1).strip("\"'") if match else None


def validate_cases(
    skill_dir: Path, skill_name: str, errors: list[str], set_case_ids: set[str], root: Path = ROOT
) -> None:
    cases_path = skill_dir / "evals" / "cases.json"
    cases_file = read_json(cases_path, errors, root)
    if cases_file is None:
        return
    label = cases_path.relative_to(root)
    if cases_file.get("schema_version") != 1:
        errors.append(f"{label}: schema_version must be 1")
    if cases_file.get("skill") != skill_name:
        errors.append(f"{label}: skill must be {skill_name!r}")
    if not isinstance(cases_file.get("baseline"), str) or not cases_file["baseline"].strip():
        errors.append(f"{label}: baseline must describe the comparison condition")

    cases = cases_file.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append(f"{label}: cases must be a non-empty array")
        return

    ids: set[str] = set()
    kinds: set[str] = set()
    for index, case in enumerate(cases):
        prefix = f"{label}: cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{prefix} must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not SKILL_NAME.fullmatch(case_id):
            errors.append(f"{prefix}.id must be lowercase kebab-case")
        elif case_id in ids:
            errors.append(f"{prefix}.id {case_id!r} is duplicated")
        elif case_id in set_case_ids:
            errors.append(f"{prefix}.id {case_id!r} is duplicated elsewhere in this set")
        else:
            ids.add(case_id)
            set_case_ids.add(case_id)
        kind = case.get("kind")
        if kind not in {"trigger", "task"}:
            errors.append(f"{prefix}.kind must be 'trigger' or 'task'")
        else:
            kinds.add(kind)
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append(f"{prefix}.prompt must be a non-empty string")
        if not isinstance(case.get("expected_activation"), bool):
            errors.append(f"{prefix}.expected_activation must be a boolean")
        if not isinstance(case.get("critical"), bool):
            errors.append(f"{prefix}.critical must be a boolean")
        repeats = case.get("repeats")
        if not isinstance(repeats, int) or isinstance(repeats, bool) or repeats < 1:
            errors.append(f"{prefix}.repeats must be a positive integer")
        criteria = case.get("success_criteria")
        if not isinstance(criteria, list) or not criteria or not all(
            isinstance(item, str) and item.strip() for item in criteria
        ):
            errors.append(f"{prefix}.success_criteria must be a non-empty array of strings")
        if kind == "task" and case.get("expected_activation") is not True:
            errors.append(f"{prefix}: task cases must expect activation")
        if kind == "task" and case.get("comparison_policy") not in {"uplift", "no-regression"}:
            errors.append(f"{prefix}.comparison_policy must be 'uplift' or 'no-regression'")
        if kind == "trigger" and "comparison_policy" in case:
            errors.append(f"{prefix}: comparison_policy is only valid for task cases")

    for required_kind in ("trigger", "task"):
        if required_kind not in kinds:
            errors.append(f"{label}: add at least one {required_kind!r} case")


def validate_skill(
    skill_dir: Path,
    expected_name: str,
    set_license: str,
    set_case_ids: set[str],
    validator: str | None,
    require_validator: bool,
    errors: list[str],
    warnings: list[str],
    root: Path = ROOT,
) -> None:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        errors.append(f"{skill_dir.relative_to(root)}: missing SKILL.md")
        return

    actual_name = read_skill_name(skill_file, errors, root)
    if actual_name and actual_name != expected_name:
        errors.append(
            f"{skill_file.relative_to(root)}: frontmatter name {actual_name!r} does not match {expected_name!r}"
        )
    skill_license = read_skill_license(skill_file)
    if skill_license and skill_license != set_license:
        license_path = Path(skill_license)
        if license_path.is_absolute() or ".." in license_path.parts or not (skill_dir / license_path).is_file():
            errors.append(
                f"{skill_file.relative_to(root)}: a skill license override must reference a bundled file inside the skill directory"
            )
    if not SKILL_NAME.fullmatch(expected_name):
        errors.append(f"{skill_dir.relative_to(root)}: skill directory name is not lowercase kebab-case")

    if validator:
        result = subprocess.run(
            [validator, "validate", str(skill_dir)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode:
            details = result.stderr.strip() or result.stdout.strip() or "validator returned a failure"
            errors.append(f"{skill_dir.relative_to(root)}: skills-ref failed: {details}")
    elif require_validator:
        errors.append("skills-ref is required; install requirements-dev.txt")
    else:
        warnings.append(f"{skill_dir.relative_to(root)}: skills-ref unavailable; only basic frontmatter checks ran")

    validate_cases(skill_dir, expected_name, errors, set_case_ids, root)


def validate_evaluation_claims(
    set_root: Path,
    set_name: str,
    version: Any,
    evaluation_status: Any,
    tested_runtimes: list[str],
    errors: list[str],
    root: Path,
) -> None:
    if evaluation_status != "passed" and not tested_runtimes:
        return
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        return

    report_path = set_root / "reports" / f"{version}.json"
    label = report_path.relative_to(root)
    if not report_path.is_file():
        errors.append(f"{label}: missing report for current evaluation claims")
        return
    report = read_json(report_path, errors, root)
    if report is None:
        return
    if report.get("set") != set_name:
        errors.append(f"{label}: report set does not match set.json")
    if report.get("version") != version:
        errors.append(f"{label}: report version does not match set.json")
    if evaluation_status == "passed" and report.get("status") != "passed":
        errors.append(f"{label}: evaluation_status is 'passed' but report status is not 'passed'")

    runtimes = report.get("runtimes")
    if not isinstance(runtimes, list):
        errors.append(f"{label}: runtimes must be an array")
        return
    by_name: dict[str, dict[str, Any]] = {}
    for entry in runtimes:
        if not isinstance(entry, dict) or not isinstance(entry.get("name"), str):
            continue
        name = entry["name"]
        if name in by_name:
            errors.append(f"{label}: duplicate runtime result for {name!r}")
        by_name[name] = entry
    for runtime in tested_runtimes:
        entry = by_name.get(runtime)
        if entry is None:
            errors.append(f"{label}: tested runtime {runtime!r} has no report result")
        elif entry.get("status") != "passed":
            errors.append(f"{label}: tested runtime {runtime!r} does not have a passing report result")


def validate_repo(require_validator: bool = False, root: Path = ROOT) -> tuple[list[str], list[str]]:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    validator = shutil.which("skills-ref")
    if validator is None:
        local_validator = Path(sys.executable).with_name("skills-ref")
        if local_validator.is_file():
            validator = str(local_validator)
    if require_validator and not validator:
        errors.append("skills-ref is required; install requirements-dev.txt")

    set_files = sorted((root / "sets").glob("*/set.json"))
    if not set_files:
        errors.append("sets/: no set.json files found")
        return errors, warnings

    for descriptor_path in set_files:
        set_root = descriptor_path.parent
        descriptor = read_json(descriptor_path, errors, root)
        if descriptor is None:
            continue
        label = descriptor_path.relative_to(root)
        set_name = descriptor.get("name")
        if set_name != set_root.name:
            errors.append(f"{label}: name must match directory {set_root.name!r}")
        if not isinstance(set_name, str) or not SKILL_NAME.fullmatch(set_name):
            errors.append(f"{label}: name must be lowercase kebab-case")
        if not isinstance(descriptor.get("version"), str) or not SEMVER.fullmatch(descriptor["version"]):
            errors.append(f"{label}: version must be SemVer")
        for field in ("description", "license", "evaluation_status"):
            if not isinstance(descriptor.get(field), str) or not descriptor[field].strip():
                errors.append(f"{label}: {field} must be a non-empty string")
        if descriptor.get("license") != "Apache-2.0" and not (set_root / "LICENSE").is_file():
            errors.append(f"{label}: non-default set license requires a set-local LICENSE file")

        targets = descriptor.get("target_runtimes")
        tested = descriptor.get("tested_runtimes")
        if not isinstance(targets, list) or not targets or not all(isinstance(item, str) for item in targets):
            errors.append(f"{label}: target_runtimes must be a non-empty array of runtime names")
            targets = []
        elif len(set(targets)) != len(targets):
            errors.append(f"{label}: target_runtimes contains duplicates")
        if not isinstance(tested, list) or not all(isinstance(item, str) for item in tested):
            errors.append(f"{label}: tested_runtimes must be an array of runtime names")
            tested = []
        elif len(set(tested)) != len(tested):
            errors.append(f"{label}: tested_runtimes contains duplicates")
        for runtime in tested:
            if runtime not in targets:
                errors.append(f"{label}: tested runtime {runtime!r} is not in target_runtimes")
        validate_evaluation_claims(
            set_root,
            set_name,
            descriptor.get("version"),
            descriptor.get("evaluation_status"),
            tested,
            errors,
            root,
        )

        members = descriptor.get("skills")
        if not isinstance(members, list) or not members:
            errors.append(f"{label}: skills must be a non-empty array")
            continue

        listed_dirs: set[Path] = set()
        listed_names: set[str] = set()
        set_case_ids: set[str] = set()
        for member in members:
            if not isinstance(member, dict):
                errors.append(f"{label}: each skills entry must be an object")
                continue
            member_name = member.get("name")
            relative_path = member.get("path")
            if not isinstance(member_name, str) or not SKILL_NAME.fullmatch(member_name):
                errors.append(f"{label}: each skill needs a lowercase kebab-case name")
                continue
            if member_name in listed_names:
                errors.append(f"{label}: duplicate skill name {member_name!r}")
                continue
            listed_names.add(member_name)
            if not isinstance(relative_path, str):
                errors.append(f"{label}: skill {member_name!r} needs a relative path")
                continue
            skill_dir = (set_root / relative_path).resolve()
            if not skill_dir.is_relative_to(set_root.resolve()):
                errors.append(f"{label}: skill path {relative_path!r} escapes its owning set")
                continue
            if skill_dir.name != member_name:
                errors.append(f"{label}: skill path basename must match {member_name!r}")
            if not skill_dir.is_dir():
                errors.append(f"{label}: skill directory does not exist: {relative_path}")
                continue
            listed_dirs.add(skill_dir)
            validate_skill(
                skill_dir,
                member_name,
                descriptor.get("license", "Apache-2.0"),
                set_case_ids,
                validator,
                require_validator,
                errors,
                warnings,
                root,
            )

        skills_root = set_root / "skills"
        actual_dirs = {path.resolve() for path in skills_root.iterdir() if path.is_dir()} if skills_root.is_dir() else set()
        for unlisted in sorted(actual_dirs - listed_dirs):
            errors.append(f"{unlisted.relative_to(root)}: skill directory is not listed in set.json")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--require-reference-validator",
        action="store_true",
        help="fail unless the pinned Agent Skills reference validator is installed",
    )
    args = parser.parse_args()

    errors, warnings = validate_repo(args.require_reference_validator)
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"Repository checks failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print("Repository structure and skill cases are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
