# Safety review: skill-factory 0.3.0

**Candidate:** `skill-factory` 0.3.0, source commit `184803a` (set source unchanged at `fdc4bc4`)
**Review date:** 2026-11-03
**Review scope:** All 13 member `SKILL.md` files and evaluation cases, the set descriptor, README, and effective Apache-2.0 license. No scripts, bundled assets, or other skill resources are present. The local `.agents/skills/` entries are discovery links to canonical sources, not additional packaged content.
**Review method:** Static review of candidate instructions and cases. No unreviewed code was executed. Behavioral evaluation is separate and currently pending.

## Risk rating: Moderate

The factory does not itself make domain decisions or execute tool/script integrations. However, it creates instructions that may later be used in consequential domains, works with user-provided or retrieved material, and may receive sensitive domain context. The member skills consistently require user approval, preserve uncertainty and provenance, protect sensitive information, treat embedded instructions as untrusted, and require qualified expert review for high-impact or consequential downstream use.

## Findings and gates

### No static-review blocker identified

- **Evidence:** Discovery, authoring, research, domain-modeling, safety, evaluation, tool-integration, runtime, release, and maintenance instructions were reviewed alongside their evaluation prompts. The cases use illustrative scenarios rather than real personal records or credentials. No executable scripts or bundled resources were found.
- **Safeguards:** Skills prohibit unsupported authority and runtime claims, require approval at scope gates, protect private context, and distinguish safety review from professional certification and behavioral evidence. The tool-integration skill only specifies and reviews integrations; it does not grant access, execute code, or build a sandbox.
- **Verification:** The exact candidate must be re-reviewed if its contents change before release.

### Behavioral evidence remains a release blocker

- **Evidence:** `set.json` records version `0.3.0`, `evaluation_status: pending`, and no tested runtimes. The critical-case smoke is in progress; no results have been reviewed here.
- **Required action:** Complete and review behavioral evidence for the current cases. Any critical failure or safety regression requires remediation and re-review. Do not infer a passing release from static validation.
- **Owner:** Set maintainer.

### Conditional gates for downstream use

- A domain-specific skill set for consequential use needs qualified domain-expert sign-off on that exact candidate; this generic factory review is not that sign-off.
- Any future candidate that actually uses tools or scripts needs reviewed, appropriately isolated, least-privileged sandbox evidence. The current `integrate-tools-safely` member is guidance only and contains no executable integration.

## Decision

No safety blocker was identified within this static review scope. **This is not release approval:** 0.3.0 remains blocked pending behavioral evidence and the remaining release checks. Re-review this exact candidate if its contents change.
