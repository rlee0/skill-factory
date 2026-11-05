# 12: Maintain and retire released skills

**What to build:** A skill-set owner can keep a released set trustworthy as domains, skills, and runtimes change, including safely updating or retiring capabilities.

**Blocked by:** 11: Prepare an evidence-backed set release.

**Status:** resolved

- [x] Assess which skills, evaluation cases, safety reviews, sources, and runtime claims are affected by a proposed change.
- [x] Recommend an independent set version change consistent with user-visible behavior and exact release membership.
- [x] Re-evaluate affected skills against the runtime baseline and update evidence before making new support claims.
- [x] Provide a clear path for deprecating or removing a skill and communicate the user-visible impact.
- [x] Include evaluation cases for change-impact analysis, re-evaluation decisions, versioning, deprecation, and retirement.
- [x] Keep the maintenance capability independently usable after the initial release workflow is complete.

## Comments

- Implemented in commit `76a5527`; fast-forwarded into the integration branch. Repository check, 21 unit tests, and diff check passed; `skills-ref` was unavailable, so only basic frontmatter validation ran. The 0.3.0 set remains pending evaluation with no tested-runtime claims.
