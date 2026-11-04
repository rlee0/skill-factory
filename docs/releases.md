# Set releases

Each set is versioned and released independently. Use Semantic Versioning according to user-visible behavior:

- **Major**: breaking behavior changes or removal of a member skill.
- **Minor**: compatible capabilities or skills are added.
- **Patch**: corrections that do not change the set's intended behavior.

A set release pins its exact membership and member contents. Do not bump a shared repository version when an unrelated set changes.

## Release gate

Before tagging:

1. Update the set version in `set.json` and review the corresponding changes.
2. Run repository checks and the required behavioral evaluations.
3. Confirm every critical case passes on every claimed runtime and review script content for safety.
4. Confirm the effective license is included.
5. Build and inspect the consumer archive.

Create a tag in the form `<set-name>/v<version>`, for example `skill-factory/v0.1.0`. The GitHub Actions workflow builds the set archive, attaches the passing evaluation report, and creates a **draft** GitHub release. One maintainer reviews and publishes the draft.

Before the first release, protect the `*/v*` tag pattern so only maintainers can create or change release tags. Require the `Checks` workflow on the default branch. The release workflow has `contents: write` only so it can create the draft; the CI workflow is read-only.

The consumer archive contains the set descriptor, README, license, and member skill directories. Evaluation fixtures stay in tagged source. The tagged repository source remains the full record of how the release was produced.
