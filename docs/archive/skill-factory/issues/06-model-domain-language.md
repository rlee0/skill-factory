# 06: Model domain language and decisions

**What to build:** A domain team can maintain shared domain terminology and record significant domain decisions that keep related skills consistent.

**Blocked by:** 01: Discover and approve a domain brief; 02: Map workflows to bounded skill opportunities.

**Status:** resolved

- [x] Identify ambiguous, overloaded, or conflicting terms and propose precise canonical definitions for user review.
- [x] Maintain domain terms separately from implementation details.
- [x] Stress-test important relationships and boundaries with concrete scenarios and edge cases.
- [x] Record a decision only when it is hard to reverse, surprising without context, and the result of a real trade-off.
- [x] Include evaluation cases for terminology clarification, scenario-based boundary checking, and irrelevant modeling requests.
- [x] Keep the domain-modeling capability independently usable and avoid requiring persistent domain documents when none are needed.

## Comments

- Implemented in commit `93cfe87`; merged into the integration branch as `e1f81a7`. Repository check and 16 unit tests passed; `skills-ref` was unavailable, so only basic frontmatter validation ran. Behavioral evaluations were not run.
