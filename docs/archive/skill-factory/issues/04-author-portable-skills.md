# 04: Author portable skills from an approved design

**What to build:** A maintainer can turn an approved skill-set architecture into focused, independently usable skills that follow the portable Agent Skills format.

**Blocked by:** 03: Design the set and guide the factory workflow.

**Status:** resolved

- [x] Define each skill's purpose, activation cues, boundaries, instructions, and completion criteria from the approved design.
- [x] Keep runtime-specific behavior and environment requirements explicit; do not claim untested compatibility.
- [x] Create supporting resources only when they materially improve the skill and inspect them for safety and sensitive information.
- [x] Preserve an explicit effective license and avoid repository-specific required metadata in skill frontmatter.
- [x] Include evaluation cases for authoring quality, portability, scope boundaries, and nearby irrelevant requests.
- [x] Keep the authoring capability independently usable.

## Comments

- Implemented in commit `425e1cf`; fast-forwarded into the integration branch. Repository check and all 16 unit tests passed; `skills-ref` was unavailable, so only basic frontmatter validation ran. Behavioral evaluations were not run.
