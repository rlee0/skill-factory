# 10: Adapt and validate runtime support

**What to build:** A maintainer can document runtime-specific differences and make precise support claims based only on completed evaluation evidence.

**Blocked by:** 03: Design the set and guide the factory workflow; 08: Evaluate activation and task outcomes.

**Status:** resolved

- [x] Keep portable Agent Skills behavior as the default and identify any runtime-specific instructions or requirements explicitly.
- [x] Select an intentional runtime matrix and define the evidence required for each claimed runtime.
- [x] Record exact runtime versions, model identifiers, and passing results before marking a runtime as tested.
- [x] Leave unsupported or unevaluated runtimes untested; never infer universal compatibility from one passing runtime.
- [x] Include evaluation cases for documenting runtime differences and refusing unsupported compatibility claims.

## Comments

- Implemented in commit `f8d9863`; merged into the integration branch as `6922c1f`. Repository check, 21 unit tests, and `git diff --check` passed; `skills-ref` was unavailable, so only basic frontmatter validation ran. Behavioral evaluations were not run.
