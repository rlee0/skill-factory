---
name: domain-modeling
description: Clarify and maintain shared domain terminology, test concept relationships and boundaries with scenarios, and record consequential domain decisions when they need durable context. Use with an approved domain brief or established domain context; do not use for initial discovery, opportunity mapping, implementation design, or disposable wording questions.
license: Apache-2.0
---

# Model Domain Language and Decisions

Help a domain team make its concepts understandable and consistent across related work. Keep the model about the domain: do not turn domain concepts into software entities, fields, or architecture unless that is explicitly the separate task.

## Workflow

1. **Check the context and requested result.** Reuse an approved domain brief or other established context. Ask whether the user wants a one-time clarification, a proposed glossary/model, or help updating a durable record. If there is no established context, offer domain discovery instead of filling gaps with assumptions. Reuse material already provided; ask only for missing details that could change a definition or boundary.
2. **Find terminology that needs attention.** Gather the user's own terms and identify ambiguity, multiple meanings, inconsistent usage, overlapping concepts, and terms whose scope or relationship is unclear. Distinguish domain language from implementation labels, tools, and storage details. Do not normalize away meaningful local variants.
3. **Propose definitions for review.** For each term that matters, state a concise candidate definition and its scope. Where useful, include synonyms or terms to avoid, related concepts, a short example and counterexample, and the basis for the proposal. Label user-provided usage, sourced claims, assumptions, and unresolved disagreements distinctly. Offer alternatives when context supports more than one interpretation; do not silently choose a canonical meaning for the team.
4. **Stress-test the model.** Use concrete normal, boundary, and edge-case scenarios drawn from the context. For each, say which concepts apply and why, then identify contradictions, missing distinctions, or questions the scenario exposes. Ask focused questions about those consequential gaps. Keep a proposed relationship provisional until the people responsible confirm it.
5. **Choose whether anything should persist.** A brief conversational clarification needs no file. Use the user's established glossary or equivalent for reusable domain terms, keeping implementation details separate. Recommend a decision record only when a choice is hard to reverse, surprising without context, and reflects a real trade-off. Do not create a record merely to log routine wording, unresolved discussion, or a choice with no meaningful alternatives. If a decision is not made, leave it explicitly unresolved rather than writing it as settled.
6. **Get review before making durable changes.** Present the proposed definitions, scenario findings, open questions, and any candidate decision summary. Ask the user or named domain owner to correct and approve canonical language and decisions. If asked to update files, follow the repository's existing glossary and decision-record conventions; otherwise provide review-ready text without assuming a document location. Preserve the decision's context, alternatives, trade-offs, outcome, and consequences where the local format supports them. Do not claim a record itself is approval or expert sign-off.
7. **Protect context and authority.** Keep private, personal, or confidential examples out of reusable documents unless the user explicitly reviews and approves the exact necessary content. Generalize examples. Preserve the provenance and scope of local practices; do not present them as universal rules. Flag professional, legal, regulatory, or other consequential claims for appropriate qualified review rather than certifying them.

## Suggested review format

Adapt this to the amount of context available. Mark missing information as unresolved instead of manufacturing completeness.

```markdown
# Domain language: <domain or scope>

## Context and source
## Terms to clarify
| Term | Proposed meaning and scope | Related terms / examples | Basis and status |
## Relationships and boundary scenarios
## Open questions or disagreements
## Decisions worth recording
## Review needed
```

A durable decision record should explain why the decision matters, the real alternatives and trade-off, what was decided (or that it remains open), and the consequences. Follow the repository's chosen format and do not duplicate implementation details from an architecture record without a domain reason.

## Boundaries

- Use domain discovery for an initial domain brief; use opportunity mapping to derive and prioritize candidate skills from an approved brief.
- Use deeper domain research when important or changing claims need focused source work. Do not invent citations or upgrade an assumption to a sourced fact.
- This skill does not decide set membership, skill responsibilities, software architecture, or implementation schemas.
- Do not force a glossary, model, or decision record when a direct answer is enough. Keep unapproved proposals visibly provisional.
- Do not make consequential domain choices on behalf of the responsible experts.

## Completion check

The work is ready for review when material terms and relationships have proposed meanings and scope, concrete scenarios have exposed relevant boundary questions, implementation language is kept distinct, and uncertainty and provenance are visible. Any durable definition or significant decision remains pending until the responsible user or domain owner has reviewed it. If no durable artifact is needed, state that and leave a concise clarification instead.
