---
name: release-skill-sets
description: Prepare or assess the release of a curated Agent Skills set. Use when checking that set's members, evaluation report, license, consumer archive, release tag, or draft. Do not invoke for general SemVer questions, release-note reviews, or software releases unrelated to Agent Skills.
license: Apache-2.0
---

# Release Skill Sets

Prepare an exact skill-set snapshot for consumers without overstating its compatibility or bypassing its quality gate.

## Workflow

1. **Inspect the set.** Read `set.json`, its README, member skills, and the release policy. Confirm the release includes only the intended members and their exact source contents.
2. **Choose the version.** Apply the set's SemVer rules: major for breaking behavior or a removed skill, minor for compatible capabilities or additions, patch for corrections. Update only this set's version.
3. **Check readiness.** Run `python3 tools/check_repo.py --require-reference-validator`. Review bundled scripts and resources. Confirm the effective license is explicit and included.
4. **Verify evidence.** Require a passing report for every claimed runtime. Confirm every critical case passes, no serious safety regression exists, and each result records exact runtime/model versions. Do not turn a target runtime into a tested claim without evidence.
5. **Build and inspect.** Run `python3 tools/build_set.py <set-name> --for-release --output dist`. Inspect the archive contents; it should contain the descriptor, README, license, and member skills, not evaluation fixtures.
6. **Prepare the draft.** Create the `<set-name>/v<version>` tag only after review. The CI workflow builds the archive, attaches the evaluation report, and creates a GitHub draft release.
7. **Hand off for approval.** Summarize the version change, evaluation results, archive contents, compatibility claims, and any limitations. A maintainer publishes the draft after review.

## Safety and completion criteria

- Do not publish a release when validation fails, a required report is missing, or a critical case fails.
- Do not run release commands that mutate a remote unless the user has explicitly approved that action.
- A release candidate is ready only when its set snapshot, report, license, archive, tag, and notes agree on the set name and version.
