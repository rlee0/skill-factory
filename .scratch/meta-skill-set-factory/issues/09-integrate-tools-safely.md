# 09: Integrate tools safely

**What to build:** A maintainer can design tool-using skills with explicit requirements and safeguards, while preventing unsupported tool behavior from being claimed as tested.

**Blocked by:** 04: Author portable skills from an approved design; 07: Review safety and obtain expert sign-off; 08: Evaluate activation and task outcomes.

**Status:** resolved

- [x] Identify required tools, permissions, credentials, environment assumptions, and failure modes before adding an integration.
- [x] Inspect scripts and supporting resources for unsafe behavior and minimize privileges and sensitive-data exposure.
- [x] Document runtime-specific requirements and safe behavior when tools or credentials are unavailable.
- [x] Require an appropriate sandboxed evaluation path before claiming tool behavior as tested; otherwise mark it untested and block unsupported release claims.
- [x] Do not build a universal sandbox as part of this capability.
- [x] Include evaluation cases for missing tools, denied permissions, unsafe tool instructions, and honest reporting of untested behavior.

## Comments

- Implemented in commit `a4913ca`; merged into the integration branch as `90b296f`. Repository check, 21 unit tests, and `git diff --check` passed; `skills-ref` was unavailable, so only basic frontmatter validation ran. Behavioral evaluations were not run.
