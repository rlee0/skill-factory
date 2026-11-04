---
name: map-skill-opportunities
description: Turn an approved domain brief and its workflows into a focused, prioritized map of bounded agent-skill opportunities. Use to identify candidate responsibilities, triggers, nearby non-triggers, non-goals, value, feasibility, risk, and evidence; do not use for initial domain discovery, set architecture, or skill authoring.
license: Apache-2.0
---

# Map Skill Opportunities

Help a domain expert decide which recurring tasks are worth supporting with agent skills and where each candidate begins and ends. This capability is independently usable; it does not require a factory coordinator.

## Workflow

1. **Check readiness.** Use the approved domain brief as the source of scope. If there is no brief or approval is unclear, ask whether the user wants discovery or can provide the reviewed brief. Do not silently treat an informal description as approved. Reuse any brief already in context.
2. **Extract work, not topics.** Identify recurring user tasks, decisions, handoffs, inputs, and outputs in the brief. For each plausible opportunity, state the person doing the work, the situation that starts it, and the useful result. Do not turn domain nouns or every workflow step into a separate skill by default.
3. **Shape candidate boundaries.** For each candidate, describe:
   - the intended user and concrete trigger;
   - nearby requests that should not activate it;
   - the responsibility and expected user-visible outcome;
   - explicit non-goals, limits, and handoffs to a person or another capability;
   - dependencies, constraints, and the brief evidence supporting the candidate.

   Keep a candidate focused enough to have one coherent responsibility and outcome. Split it when workflows have materially different users, triggers, decisions, or risk boundaries. Combine candidates when they serve the same user in the same workflow and separating them would duplicate work; make any handoff explicit.
4. **Review the inventory.** Find and explain overlapping responsibilities, candidates that are too broad, low-value or infeasible proposals, and important recurring work with no candidate. Distinguish a genuine missing capability from a gap that needs more information. Do not preserve a proposal just because it was suggested.
5. **Prioritize transparently.** Order the candidates worth pursuing, considering:
   - **User value:** frequency or importance of the need and the likely improvement;
   - **Feasibility:** whether a skill can help with available context, authority, tools, and constraints;
   - **Risk:** harm from a mistaken or overconfident response and the safeguards or human review needed;
   - **Evidence:** how clearly the approved brief supports the need and boundary.

   Give a short, case-specific rationale for each factor. Qualitative labels are enough; do not invent numeric precision, frequency, evidence, or certainty. Mark assumptions and open questions as such. High risk is a reason for caution or expert review, not a reason to silently broaden a skill's authority.
6. **Return a reviewable map.** Present a concise ordered shortlist with the candidate boundaries above, then list merge/split/defer/reject recommendations and material gaps. Identify which evidence came from the brief, which interpretation is provisional, and what needs an answer. Ask the user to correct and approve the proposed opportunities before set architecture or authoring begins. Approval of this map is not approval of later implementation or packaging.

## Output shape

Adapt this outline to the amount of information available; say “not provided” or “unresolved” rather than filling gaps by guessing.

```markdown
# Skill opportunity map: <domain>

## Basis and open questions
## Prioritized opportunities
### <candidate name>
- User and workflow:
- Trigger:
- Nearby non-triggers:
- Responsibility and expected outcome:
- Non-goals and handoffs:
- Value / feasibility / risk / evidence:
## Overlap, broad or low-value proposals
## Missing capabilities or information
## Review decision
```

## Boundaries

- Do not restart domain discovery when the brief is approved; ask only focused questions that materially affect candidate boundaries or priority.
- Do not present an unverified user claim, assumption, or missing detail as a sourced fact. Do not claim that a proposed skill is effective or safe without evaluation evidence.
- Do not include unnecessary personal or confidential information from the brief in reusable skill proposals. Generalize examples and retain only constraints needed to make a boundary clear.
- Do not design final set membership, runtime support, implementation architecture, or write candidate skills. Hand the approved map to those next phases.
- Do not make consequential decisions on behalf of domain experts. Flag candidates that need qualified review and describe a safe human handoff.

## Completion check

The map is ready for review when its shortlist is derived from approved workflows, candidates have actionable triggers and explicit responsibilities and non-goals, nearby non-triggers are clear, overlap/breadth/value/gaps are addressed, and priorities explain value, feasibility, risk, and evidence without invented certainty. Keep it pending until the user has had a chance to correct and approve it.
