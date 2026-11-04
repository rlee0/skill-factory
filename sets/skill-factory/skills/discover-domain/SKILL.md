---
name: discover-domain
description: Help a domain expert discover and review the context for an agent skill set. Use when eliciting users, workflows, outcomes, constraints, terminology, edge cases, risks, sources, or uncertainty and preparing a domain brief; do not use to prioritize skill candidates from an already approved brief.
license: Apache-2.0
---

# Discover a Domain

Help a domain expert turn what they know about their area into a concise, reviewable domain brief. This skill is useful on its own; no factory coordinator is required.

## Workflow

1. **Invite the story.** Ask the user to describe their area and what they hope an agent skill set could help with, in their own terms. Reuse information already provided; do not make them repeat it or start with a long questionnaire.
2. **Explore the work.** Elicit, in focused conversational turns:
   - who does the work and who is affected;
   - recurring workflows, including decisions, handoffs, and existing tools where relevant;
   - desired outcomes and how people recognize success;
   - constraints such as time, access, policy, language, resources, or environment;
   - domain terms and what they mean in context;
   - representative exceptions, edge cases, and points where work becomes difficult;
   - known risks, sensitive information, and actions an agent must not take.

   Ask only questions that materially improve the brief. If a detail is not essential yet, mark it unresolved instead of blocking progress.
3. **Resolve consequential gaps.** Identify missing facts that could change the domain scope, safety boundary, or intended users. Ask a small number of specific follow-up questions, explaining why an answer matters when helpful. Do not fill gaps with guesses. If the user cannot answer, retain the uncertainty in the brief.
4. **Track the basis for claims.** Keep four categories distinct:
   - **User-provided:** the user's description or stated local practice; it is not independently verified.
   - **Sourced:** a fact checked against a trustworthy source. For claims that materially affect the brief, prefer a relevant primary source where available and record its name, link, and date. Note which claim it supports.
   - **Assumption:** a provisional interpretation that still needs confirmation.
   - **Unresolved:** a question, missing source, or disagreement that remains open.

   Ground important domain claims when appropriate and possible. Honor a request to defer research; list verification as an open item instead. If sources are unavailable, stale, or conflicting, say so rather than upgrading a claim to fact. Deeper source-intensive research is a separate task.
5. **Surface preliminary risks.** Note risks that affect the brief, including possible harm, privacy, unequal access, sensitive data, and consequential decisions. Ask what safeguards or limits the expert already knows. Mark professional or jurisdiction-specific claims for qualified review where needed; a brief is not legal, clinical, regulatory, or other professional certification.
6. **Write a compact domain brief.** Include the following headings, using “not provided” or “unresolved” instead of inventing completeness:

   ```markdown
   # Domain brief: <working title>

   ## Purpose and intended users
   ## People affected
   ## Recurring workflows
   ## Desired outcomes and success signals
   ## Constraints and boundaries
   ## Terminology
   ## Representative edge cases
   ## Preliminary risks and safeguards
   ## Evidence and provenance
   ## Assumptions and unresolved questions
   ## Sensitive context to exclude from packaged skills
   ## Decisions requiring expert or user review
   ```

   Keep it useful for later skill planning, not an exhaustive domain manual. Include only context needed to design the skill set.
7. **Review and obtain approval.** Summarize the most important scope choices and uncertainties. Invite corrections, then ask the user to approve this brief or request changes. Treat approval as permission to use the reviewed brief for the next planning phase, not as approval of skills or of packaging private context.

## Privacy and packaging

- Prefer generalized, de-identified examples. Do not request personal records or unnecessary sensitive details.
- Keep discovery notes and personal or confidential context out of packaged skills by default. Include a sensitive detail only when the user explicitly reviews and approves that exact content for inclusion and it is necessary; otherwise retain a generalized constraint or omit it.
- Do not turn a user's account of a policy or practice into a universal rule. Preserve its provenance and scope.

## Completion check

A domain brief is ready for review when it covers the known users, workflows, outcomes, constraints, terminology, edge cases, and preliminary risks; separates user-provided claims, sourced facts, assumptions, and unresolved questions; identifies sensitive context to exclude and decisions needing review; and has been shown to the user for correction and approval. If a required detail remains unknown, state that clearly and leave the brief pending approval rather than silently resolving it.
