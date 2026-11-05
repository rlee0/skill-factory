# 03: Design the set and guide the factory workflow

**What to build:** A domain expert can approve a tailored skill-set architecture and follow a coordinator through the factory's major decisions and phase handoffs.

**Blocked by:** 01: Discover and approve a domain brief; 02: Map workflows to bounded skill opportunities.

**Status:** resolved

- [x] Define set membership, responsibilities, handoffs, runtime assumptions, and conditional capabilities from the approved brief and opportunity map.
- [x] Prefer a lean core and include specialist capabilities only when domain, risk, tool use, or release needs justify them.
- [x] Guide the user through scope and architecture approval before authoring or packaging begins.
- [x] Track accepted decisions and unresolved questions through the workflow without duplicating phase-skill responsibilities.
- [x] Allow users to enter through the coordinator or use a phase skill independently.
- [x] Include evaluation cases for end-to-end intake, approvals, handoffs, and architecture output, as well as nearby irrelevant requests.

## Comments

- Implemented in commit `3cf6547`; merged into the integration branch as `4723478`. Repository check and 16 unit tests passed; `skills-ref` was unavailable, so only basic frontmatter validation ran. Behavioral evaluations were not run.
