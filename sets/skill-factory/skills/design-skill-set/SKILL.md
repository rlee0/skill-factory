---
name: design-skill-set
description: Design only the architecture for a skill set from an approved domain brief and opportunity map, including requesting missing artifact contents needed to proceed. Define lean membership, responsibilities, handoffs, runtime assumptions, and justified optional capabilities; do not coordinate the whole factory workflow, restart discovery, remap opportunities, or author skills.
license: Apache-2.0
---

# Design a Skill Set

Use this skill independently to turn approved domain context and opportunities into a reviewable architecture. It designs membership and boundaries; it does not write member skills or require a factory coordinator.

## Workflow

1. **Check the inputs.** Work from a user-approved domain brief and approved skill-opportunity map. Reuse artifacts already in context. If approval or an input is missing or ambiguous, ask for the reviewed artifact or offer the appropriate earlier phase (`discover-domain` or `map-skill-opportunities`). Do not treat a draft as approved or silently redo those phases.
2. **Trace the design.** For each proposed member, identify which approved opportunity or cross-cutting need justifies it. Preserve the source's provenance, constraints, risk limits, unresolved questions, and approval state. Do not turn assumptions into requirements.
3. **Choose a lean membership.** Propose only capabilities needed to deliver the approved outcomes. Use the opportunity map's boundaries to decide whether work belongs in one skill or separate skills. For each member define:
   - name and purpose;
   - intended user and situation/trigger;
   - responsibility and user-visible result;
   - explicit non-goals and authority limits;
   - inputs, outputs, dependencies, and handoffs to another member or a person;
   - the approved evidence and rationale for inclusion.

   Check for duplicate responsibilities, gaps, unnecessary members, and broad skills that combine different users, workflows, or risk boundaries. Prefer an explicit human handoff over giving a skill authority the brief does not grant.
4. **Assess optional capabilities.** Keep specialist capabilities out unless the approved context justifies them. Consider:
   - deeper source research (for example, `research-domain`) for consequential, changing, disputed, or evidence-intensive claims;
   - durable domain modeling for extensive shared terminology, rules, or cross-skill decisions that need maintenance;
   - tool/script integration (`integrate-tools-safely`) when an authorized tool materially improves the workflow; use it to specify safeguards and determine whether an appropriate sandboxed evaluation path is available;
   - runtime-specific adaptation only when a named runtime has a concrete requirement not met by the portable design.

   State the case-specific need, boundaries, dependencies, and review/evaluation requirement for each included specialist. Otherwise mark it deferred or not needed; do not add capabilities speculatively.
5. **State runtime assumptions honestly.** Prefer portable Agent Skills behavior. Record intended runtimes and any actual runtime-specific assumptions. A target runtime is not a tested runtime: claim tested support only when passing evaluation evidence records the exact runtime version and model. Mark unknown compatibility untested.
6. **Present and gate the architecture.** Return a compact design for user review, including unresolved decisions and the effect of each material choice. Invite corrections and ask for explicit approval or requested changes. Keep the design pending until approval. Approval authorizes the next authoring phase only; it does not approve implementation details, packaging, safety review, or release.

## Output shape

Adapt this outline to the available approved material. Say “not provided” or “unresolved” rather than filling gaps by guessing.

```markdown
# Skill-set architecture: <working title>

## Approved basis and scope
## Proposed core members
### <member name>
- Opportunity / evidence:
- User and trigger:
- Responsibility and outcome:
- Non-goals and authority limits:
- Inputs, outputs, dependencies, and handoffs:
## Optional capabilities
## Overlap, gaps, and deferred decisions
## Runtime assumptions and evidence status
## Approval decision
```

## Boundaries

- Do not perform initial domain discovery, re-prioritize opportunities, or silently change an approved scope. Route those requests to `discover-domain` or `map-skill-opportunities`.
- Do not author member instructions, create evaluation evidence, build archives, or claim a design is implemented or tested.
- Do not add tools, scripts, specialist members, or runtime-specific behavior without a need grounded in approved context and a viable review path.
- Do not include private discovery notes or sensitive details in reusable architecture unless their exact inclusion is necessary, explicitly reviewed, and approved.
- Flag consequential or professional decisions for qualified human review; architecture is not domain certification.

## Completion check

The architecture is ready for decision when every member traces to approved evidence, roles and handoffs are distinct, optional capabilities have explicit justification or are deferred, runtime claims are evidence-based, unresolved choices remain visible, and the user has been asked to approve the design before authoring or packaging.
