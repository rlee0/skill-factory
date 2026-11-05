# 07: Review safety and obtain expert sign-off

**What to build:** A maintainer can identify and address risks in a proposed or authored skill set, with qualified expert review required for high-impact or consequential skills.

**Blocked by:** 03: Design the set and guide the factory workflow; 04: Author portable skills from an approved design.

**Status:** resolved

- [x] Scale review depth to domain impact, intended users, tool access, and potential consequences.
- [x] Review domain harms, sensitive information, prompt-injection exposure, supporting resources, scripts, and tool behavior where applicable.
- [x] Define mitigations and release-blocking issues in terms the maintainer can act on.
- [x] Require qualified domain-expert review and sign-off for high-impact or consequential skills; never imply that the factory itself provides professional certification.
- [x] Recheck mitigations and sign-off before release; critical safety regressions block release.
- [x] Include evaluation cases for risk identification, unsafe requests, sensitive-context handling, and cases where expert review is required.

## Comments

- Implemented in commit `a10f266`; merged into the integration branch as `91668c0`. Repository check and all 16 unit tests passed; `skills-ref` was unavailable, so only basic frontmatter validation ran. Behavioral evaluations were not run.
