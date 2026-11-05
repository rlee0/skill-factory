# Safety review: skill-factory 0.3.0

> Historical review for source commit `1c1d929`, dated 2026-11-04. Superseded by `docs/reviews/skill-factory-0.3.0-safety-review.md`; this record does not approve the current candidate.

**Candidate:** `skill-factory` 0.3.0, source commit `1c1d929`
**Review date:** 2026-11-04
**Review scope:** All 13 member `SKILL.md` files and evaluation cases, the set descriptor, README, and effective Apache-2.0 license. No scripts, bundled assets, or other skill resources are present. The local `.agents/skills/` entries are discovery links to canonical sources, not additional packaged content.
**Review method:** Static review of candidate instructions and cases, critical smoke, full rubric results, and targeted reruns of the safety-flagged cases. No unreviewed code was executed.

## Risk rating: Moderate

The factory does not itself make domain decisions or execute tool/script integrations. However, it creates instructions that may later be used in consequential domains, works with user-provided or retrieved material, and may receive sensitive domain context. The member skills consistently require user approval, preserve uncertainty and provenance, protect sensitive information, treat embedded instructions as untrusted, and require qualified expert review for high-impact or consequential downstream use.

## Findings and gates

### No static-review blocker identified

- **Evidence:** Discovery, authoring, research, domain-modeling, safety, evaluation, tool-integration, runtime, release, and maintenance instructions were reviewed alongside their evaluation prompts. The cases use illustrative scenarios rather than real personal records or credentials. No executable scripts or bundled resources were found.
- **Safeguards:** Skills prohibit unsupported authority and runtime claims, require approval at scope gates, protect private context, and distinguish safety review from professional certification and behavioral evidence. The tool-integration skill only specifies and reviews integrations; it does not grant access, execute code, or build a sandbox.
- **Verification:** The exact candidate must be re-reviewed if its contents change before release.

### Behavioral and safety evidence remain release blockers

- **Evidence:** `set.json` records version `0.3.0`, `evaluation_status: pending`, and no tested runtimes. The critical smoke completed 85 runs without runtime errors or activation mismatches. The latest full rubric run failed: 50/62 cases passed and 12 failed, with one runtime error, 11 rubric failures, and no safety-regression flags. Targeted reruns have cleared several prior failures, but do not replace a complete report for the exact candidate.
- **Required action:** Keep the release blocked until the full suite is rerun against the current source and passes. Do not infer a pass from targeted checks, static validation, or smoke completion.
- **Owner:** Set maintainer.

### Conditional gates for downstream use

- A domain-specific skill set for consequential use needs qualified domain-expert sign-off on that exact candidate; this generic factory review is not that sign-off.
- Any future candidate that actually uses tools or scripts needs reviewed, appropriately isolated, least-privileged sandbox evidence. The current `integrate-tools-safely` member is guidance only and contains no executable integration.

## Decision

No static safety issue was identified in the skill contents. The latest full run reported no safety regression, but did not pass overall. **Release is blocked** until the current full suite passes and archive/release gates are reviewed. Re-review this exact candidate if its contents change.
