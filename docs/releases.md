# Set releases

Each set is versioned and released independently. Use Semantic Versioning according to user-visible behavior:

- **Major**: breaking behavior changes or removal of a member skill.
- **Minor**: compatible capabilities or skills are added.
- **Patch**: corrections that do not change the set's intended behavior.

A set release pins its exact membership and member contents. Do not bump a shared repository version when an unrelated set changes.

## Release gate

Before tagging, validate the same exact source revision that will be tagged. An archive that builds is not evidence that the set is ready:

1. Review `set.json`, the human-readable overview, exact member directories and contents, evaluation fixtures, and independent SemVer change. Preserve old reports; the current report must identify the current set version.
2. Run repository checks and review the complete passing behavioral report for every claimed runtime. Every authored case must be present with complete evidence; all critical cases must pass and no safety regression may exist. Keep targets with incomplete evidence untested.
3. Require a documented safety/security review of the exact candidate. Unresolved critical findings block release. For consequential use, require recorded sign-off from a qualified domain expert on that candidate; the safety review is not a substitute.
4. For any tool- or script-using member, require appropriately isolated, least-privileged sandbox evidence for tool behavior. Prompt-only evaluation and repository checks are insufficient; absent evidence blocks the candidate release while the integration remains included. Remove/defer it or obtain the required evidence before review.
5. Confirm the effective license and all required license files are explicit and will be included.
6. Run repository checks and `python3 tools/build_set.py <set-name> --for-release --output dist`, then inspect the archive against the exact source: descriptor, README, effective license, declared members and contents present; evaluation fixtures and undeclared/private files absent. Record its checksum and inspection in the handoff.
7. Have a maintainer review the version, evidence, safety decision, required expert/sandbox records, and archive before creating the tag. The builder validates the report contract; it does not authenticate evidence or enforce safety review, expert sign-off, or sandbox evidence.

Create a tag in the form `<set-name>/v<version>`, for example `skill-factory/v0.1.0`. The GitHub Actions workflow builds the set archive, attaches the passing evaluation report, and creates a **draft** GitHub release. One maintainer reviews and publishes the draft.

Before the first release, protect the `*/v*` tag pattern so only maintainers can create or change release tags. Require the `Checks` workflow on the default branch. The release workflow has `contents: write` only so it can create the draft; the CI workflow is read-only.

The consumer archive contains the set descriptor, README, license, and member skill directories. Evaluation fixtures stay in tagged source. Keep generated archives out of commits unless explicitly required. The tagged repository source remains the full record of how the release was produced. Do not create or modify remote tags or releases without explicit authorization.
