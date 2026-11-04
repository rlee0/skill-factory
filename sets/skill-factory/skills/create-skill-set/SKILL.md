---
name: create-skill-set
description: Coordinate a domain expert through the approved phases for creating and maintaining an evidence-backed agent skill set, tracking decisions, approvals, unresolved questions, and handoffs without duplicating phase skills.
license: Apache-2.0
---

# Create a Skill Set

Guide a domain expert through the factory workflow from their current state, not from a fixed script. This skill coordinates phase handoffs and approval gates; it does not replace the independently usable phase skills.

## Start from the user's state

1. Reuse the user's context and any domain brief, opportunity map, architecture, skill files, evaluation results, safety review, or release evidence already provided. Ask what they want to accomplish if the goal is unclear; do not make them repeat known information.
2. Establish which artifacts are reviewed and explicitly approved, which are drafts, and which decisions remain open. Do not infer approval from a request to “continue,” a draft, or approval of an earlier phase.
3. If the user asks for only one independent phase, direct them to that phase skill or help with that bounded phase without forcing the complete coordinator workflow. Use this skill when they want the phases coordinated or need the next safe handoff.

## Workflow and gates

Advance only as far as the available inputs and user approvals permit. Name the next phase, its input, and the artifact it should return. If a phase skill is available, hand off to it; otherwise explain the handoff and ask the user to bring its output back. Do not claim to have run a phase that was not performed.

1. **Discover the domain — `discover-domain`.** If there is no reviewed domain brief, start from the user's story and hand off discovery. Ask the user to review and explicitly approve the brief's scope before mapping. Keep private discovery notes out of reusable artifacts by default.
2. **Map opportunities — `map-skill-opportunities`.** With an approved brief, hand off workflow-to-opportunity mapping. Do not redo discovery. Ask the user to review and approve the proposed opportunities before architecture design.
3. **Design membership — `design-skill-set`.** With the approved brief and map, hand off membership, responsibilities, handoffs, runtime assumptions, and conditional-capability decisions. Present the resulting architecture for correction and explicit approval. **Do not begin authoring, implementation, or packaging until this architecture is approved.**
4. **Integrate tools when justified — `integrate-tools-safely`.** Before implementing an approved tool/script capability, specify its least-privilege permissions, credential handling, runtime assumptions, inspected resources, and safe failure behavior. Require a sandboxed evaluation path; without one, leave tool behavior untested and block its tested/safe/support and release claims.
5. **Author — `author-skills`.** After architecture approval and any required integration plan, author only the approved members. Keep each skill independently usable and portable; return implementation decisions or unresolved questions to the user rather than silently changing the architecture.
6. **Evaluate — `evaluate-skills`.** Create and run relevant and nearby-irrelevant trigger cases and representative task cases for each skill, plus coordinator workflow cases. Compare task outcomes against the same runtime baseline where practical. Record exact runtime, version, model, loaded skill IDs, results, and repeats. If evaluation cannot run, retain runnable cases and mark the runtime untested; never invent passing evidence. Tool behavior needs a separate appropriate sandboxed path.
7. **Review safety — `review-safety`.** Require a risk-scaled safety and security review before release. Obtain qualified expert review and sign-off for high-impact or consequential behavior. Ordinary prompt/task evaluation is not evidence that tool behavior is safe.
8. **Prepare release — `release-skill-set`.** Release only after structural checks, required behavioral evidence, safety review, expert sign-off when applicable, license and version decisions, and consumer-archive inspection are complete. Critical evaluation failures, serious safety regressions, or missing required evidence block a passing release. Keep drafts and untested artifacts explicitly marked as such.
9. **Maintain — `maintain-skill-set`.** For later changes, identify affected skills and runtime claims, rerun relevant evaluations and reviews, decide version changes, and manage deprecation or retirement. Do not assume old evidence covers changed behavior.

### Conditional handoffs

Include specialist work only when the approved context warrants it: deeper source research (`research-domain`) for consequential, changing, disputed, or evidence-intensive claims; durable domain modeling when terminology or rules need shared maintenance; tool/script integration (`integrate-tools-safely`) when authorized tools materially improve the work, including to establish whether a sandboxed evaluation path exists; and runtime-specific adaptation for a concrete named-runtime need. If no suitable sandbox exists, preserve that blocker and leave the tool behavior untested. A conditional phase is not a default prerequisite for every set.

## Approval and workflow state

Keep a compact workflow ledger in the conversation and, when useful, offer it as a user-reviewed Markdown artifact. Do not store sensitive discovery details in the ledger or put them into packaged skills without exact, necessary, explicit user approval. Track:

| Phase/artifact | State | Approved decision or open question | Next handoff |
| --- | --- | --- | --- |
| Domain brief | Not started / in progress / awaiting review / approved | Scope and unresolved items | `discover-domain` or `map-skill-opportunities` |
| Opportunity map | Not started / in progress / awaiting review / approved | Accepted, deferred, or rejected candidates | `map-skill-opportunities` or `design-skill-set` |
| Architecture | Not started / in progress / awaiting review / approved | Membership and open design choices | `design-skill-set` or `author-skills` |
| Skills, evaluations, safety, release, maintenance | Not started / in progress / blocked / complete | Evidence and outstanding gates | Corresponding phase skill |

Use “approved” only after the user explicitly approves that artifact. Preserve accepted decisions and unresolved questions across handoffs, and identify when a new decision supersedes an earlier one. If scope changes, return to the affected approval gate instead of carrying the old approval forward.

## Response pattern

For each coordinator turn:

1. Summarize the user's current phase and the evidence/approval state in a few lines.
2. Name the next safe handoff and what input it will use or return.
3. State any approval gate or blocker plainly.
4. Ask only for the next material decision or artifact. Do not present a long questionnaire or downstream work before the gate is met.

## Boundaries

- Do not duplicate domain discovery, opportunity mapping, architecture, authoring, evaluation, safety review, release, or maintenance work owned by phase skills. Coordinate and preserve their outputs instead.
- Do not skip user review of domain scope/opportunities or architecture, and do not treat approval of one artifact as approval of another.
- Do not make domain decisions, professional judgments, or runtime compatibility claims on the user's behalf.
- Do not fabricate phase completion, evaluation results, safety sign-off, expert approval, or release status.
- Do not move to packaging or claim a passing release while critical evidence, required safety review, or applicable expert sign-off is missing.

## Completion check

A coordinator handoff is ready when the current phase and approval state are clear, accepted decisions and unresolved questions remain visible, sensitive context is not copied unnecessarily, the next phase skill has a defined input and expected output, and no approval or evidence gate has been skipped.
