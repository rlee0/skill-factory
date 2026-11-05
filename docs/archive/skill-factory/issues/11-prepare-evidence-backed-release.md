# 11: Prepare an evidence-backed set release

**What to build:** A maintainer can prepare a reproducible, repository-ready set release whose declared contents, license, evidence, and consumer archive agree.

**Blocked by:** 04: Author portable skills from an approved design; 05: Research source-intensive domains; 06: Model domain language and decisions; 07: Review safety and obtain expert sign-off; 08: Evaluate activation and task outcomes; 09: Integrate tools safely; 10: Adapt and validate runtime support.

**Status:** resolved

- [x] Validate the set descriptor, human-readable overview, exact membership, skill contents, and evaluation evidence using repository conventions.
- [x] Apply independent semantic versioning and make the effective license explicit.
- [x] Require all critical cases to pass on each claimed runtime, safety review to pass, and required expert sign-off to be present.
- [x] If behavioral evaluation is unavailable, mark the runtime untested or release blocked; do not create a passing report or unsupported claim.
- [x] Build and inspect a consumer archive that includes the declared set contents and license while keeping evaluation fixtures in tagged source.
- [x] Ensure the release represents an exact membership and content snapshot and is not published until maintainer review.

## Comments

- Implemented in commit `efa0702`; merged into the integration branch as `4d2f325`. Repository check, 21 unit tests, and diff check passed. A non-release archive was inspected; the release build correctly remained blocked because evaluation is pending. No live behavioral evaluation or tag was created.
