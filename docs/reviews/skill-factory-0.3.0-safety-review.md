# Safety review: skill-factory 0.3.0

**Candidate:** `skill-factory` 0.3.0, source commit `a007f1dc28bc10ef5225d75932d6467a6a45d1ba` (based on `e1c8c56c23b11e578b43cdf03af4358b51676017`); evaluated-content digest `sha256:0946b38318deebbf19c061ca9ef4afc65cafb489966227cf8c4017191aa219e2`; release-candidate tree digest excluding reports `sha256:ae0f3c998473963f576fd10dd77491beccbdde6979f783fe819b3462d488104d`.
**Review date:** 2026-11-05
**Prior review:** The initial review dated 2026-11-04 covered source commit `1c1d929` only.
**Review scope:** The exact current set descriptor, README, effective Apache-2.0 license, all 13 member skill instructions and evaluation cases, canonical report, and human-adjudication records. The package contains no executable integrations, scripts, or bundled assets; local `.agents/skills/` entries are discovery links to canonical member skills.
**Review method:** Compared current set content with the initial review; inspected all 11 changed skill/case files; reviewed merged-report provenance, retained automated votes, human-adjudication rationale, validator constraints, and the release-mode archive. No real inventory, customer data, production credential, or proposed helper was accessed or executed. The separate report-builder/evaluation code is not packaged; its relevant report-contract tests were reviewed, but this is not a general code-security audit.

## Risk rating: Moderate

The factory does not itself make domain decisions or execute tool/script integrations, but it creates instructions that may be used in consequential domains and can process user-provided or retrieved material. It may receive sensitive context. The current content sets approval and privacy boundaries, requires uncertainty and provenance to be preserved, treats embedded instructions as untrusted, and requires qualified expert review for high-impact downstream skill sets.

## Findings and gates

### No static safety blocker identified within scope

- **Privacy and sensitive content:** `author-skills` keeps private interview/customer notes out by default, requires necessity and exact-content review, and separates owner approval to include material from approval to distribute it. Its evaluation case uses unavailable illustrative files and explicitly prohibits asking the user to paste private notes.
- **Tool and credential boundaries:** `integrate-tools-safely` remains design/review guidance only. It requires least-privilege, test-only non-production credentials or none, synthetic test data, network controls, safe-failure tests, source review, and reviewer-confirmed passing evidence. It grants no access and executes no helper. The untrusted-instructions case treats environment-variable upload as exfiltration and keeps unavailable code unexecuted pending review.
- **Release and maintenance claims:** `release-skill-set` blocks claims and release when reviewed passing sandbox evidence, safety review, or other gates are missing. `maintain-skill-set` scopes evidence to exact retained runtime/model claims and the current candidate. Neither directs publication or overwriting historical evidence.
- **Research and safety reviews:** Updated criteria require unresolved research claims to remain unsourced until sources are accessible and verified, and require exact candidate materials and intended-use context before safety findings or sign-off are claimed.
- **Evaluation/report safeguards:** The canonical R13 report preserves the three automated votes and requires rationale for each human score that differs. Human adjudication cannot override runtime errors, activation failures, or any safety-regression vote. Reviewer attribution is supplied by the report author and is not cryptographically authenticated; the repository's required human approval process remains necessary.
- **Distribution:** The report includes all 62 cases: 23 affected cases were refreshed, and 39 unchanged results were reused only after verifying case definitions and confirming that no changed member skill was loaded. No safety regressions were reported. Raw response artifacts and the review packet remain local and are not included in the report or archive.

### Local release candidate prepared; publication remains blocked

- **Behavioral report:** `sets/skill-factory/reports/0.3.0.json` has `status: passed` and validates for OpenCode `opencode v2.2.5` / `opencode/gpt-6-luna`. `set.json` records `evaluation_status: passed` and `tested_runtimes: [OpenCode]`. The evaluated-content digest and final release-candidate tree digest are recorded in the report provenance; the descriptor's only post-evaluation change was this evidence-status metadata.
- **Release-mode archive inspection:** The local `skill-factory-0.3.0.zip` contains the exact 13 declared members and 16 package files, byte-for-byte matching the current source. Evaluation fixtures, reports, and scratch artifacts are absent. SHA-256: `f4a9b4ee1d9bc1b1b0272f5e1a2c791763988ef18a27facf3312c970e423cc5f`. The `evaluation-report.json` sidecar matches the canonical report.
- **Outstanding release gate:** A maintainer must review the exact report, safety decision, and inspected archive before any tag or draft release. No tag, draft, remote release, or publication has been created. This safety review does not authorize those actions.

### Conditional downstream gates

- This generic factory's intended use is not itself a consequential domain decision, so this review does not require domain-expert sign-off for the factory. A downstream skill set used in a high-impact or consequential domain still requires qualified expert sign-off for that exact candidate.
- Any future candidate that executes a tool or script must have reviewed, appropriately isolated sandbox evidence for the exact behavior. The present integration member is guidance only; no actual helper or production integration was tested.

## Decision

No static safety blocker was identified within the stated scope. The validated R13 behavioral report has no safety-regression flags, and the release-mode archive matches the current source. **The candidate is ready for maintainer review, but is not released.** This review applies only to the release-candidate tree digest recorded above; any set-content change requires review of the changed content and affected gates.
