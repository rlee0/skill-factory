# Meta-Skill Set Factory

Status: ready-for-agent

## Problem Statement

Domain experts who want an agent skill set for their area must translate domain knowledge into a useful collection of skills, yet they may not know how to discover skill opportunities, define clear boundaries, author portable skills, evaluate behavior, or prepare a trustworthy release. The current skill-factory set focuses on authoring, evaluation, and release; it does not provide a guided end-to-end path from domain discovery through post-release maintenance.

Without that path, generated skill sets risk being incomplete, overlapping, ungrounded in the domain, unsafe for their intended use, or presented as compatible without behavioral evidence.

## Solution

Create a redesigned, guided meta-skill set that helps a domain expert move from an initial request to a maintained, evidence-backed skill set. A coordinator will guide the user through discovery, opportunity mapping, architecture, authoring, evaluation, safety review, release, and maintenance. Each phase skill will also remain independently useful.

The factory will produce a lean core and add optional capabilities only when the domain, risk, tool use, or release context justifies them. It will follow this repository's canonical set format and release protocol while keeping individual `SKILL.md` files portable. The factory will require user approval at major scope and architecture gates, ground important claims in trustworthy sources when needed, and never invent evaluation evidence or runtime support.

## User Stories

1. As a domain expert new to agent skills, I want a guided intake, so that I can explain the problem in my own terms without first learning skill-authoring conventions.
2. As a domain expert, I want the factory to clarify intended users, workflows, constraints, and success outcomes, so that the generated set addresses real work rather than a broad topic label.
3. As a domain expert, I want the factory to identify uncertainty and ask focused follow-up questions, so that assumptions are not silently treated as domain facts.
4. As a domain expert, I want important domain claims grounded in trustworthy sources when appropriate, so that generated instructions do not rely solely on unsupported assertions.
5. As a domain expert, I want user-provided knowledge, sourced facts, and unresolved questions distinguished, so that I can review the basis for the generated set.
6. As a domain expert, I want the factory to identify relevant terminology, actors, workflows, and edge cases, so that skills use consistent domain language.
7. As a domain expert, I want the factory to convert workflows into candidate skill opportunities, so that the set covers actionable tasks rather than merely describing the domain.
8. As a domain expert, I want each candidate skill to have intended triggers, nearby non-triggers, responsibilities, and non-goals, so that activation and ownership boundaries are clear.
9. As a domain expert, I want the factory to identify duplicate, overly broad, or low-value candidates, so that the resulting set stays focused and avoids redundant skills.
10. As a domain expert, I want to approve the domain scope and proposed skill opportunities before authoring begins, so that the factory does not write a set based on a plan I have not accepted.
11. As a domain expert, I want to approve the set architecture and membership before implementation, so that I retain control over the set's intended capabilities.
12. As a domain expert, I want a coordinator to manage phase handoffs and decisions, so that I can complete the process without manually orchestrating every skill.
13. As a skill author, I want each phase capability to remain independently usable, so that I can run discovery, evaluation, or maintenance without invoking the full factory workflow.
14. As a skill-set maintainer, I want the factory to produce a lean core and conditionally include specialist capabilities, so that every generated set is not burdened with irrelevant skills.
15. As a skill-set maintainer, I want authored skills to use the portable Agent Skills format, so that they can work across compatible runtimes.
16. As a skill-set maintainer, I want runtime-specific behavior and environment requirements documented, so that users understand portability limits.
17. As a skill-set maintainer, I want each authored skill evaluated independently as well as through the coordinator workflow, so that the phase skills remain usable on their own and the overall process works end to end.
18. As an evaluator, I want cases for relevant triggers and nearby irrelevant prompts, so that evaluation checks both appropriate activation and restraint.
19. As an evaluator, I want representative tasks with observable criteria, appropriate repeats, and criticality, so that behavior can be assessed consistently.
20. As an evaluator, I want task outcomes compared against the same runtime baseline while preserving native runtime capabilities, so that evaluation measures the skill set's added value.
21. As a maintainer, I want exact runtime and model details recorded for evaluated results, so that compatibility claims are evidence-based and reproducible.
22. As a maintainer, I want the factory to leave an unsupported runtime untested rather than infer compatibility, so that users are not misled by aspirational claims.
23. As a safety reviewer, I want each set to receive a required, risk-scaled safety and security review, so that domain harms, tool behavior, scripts, and prompt-injection exposure are considered before release.
24. As a qualified domain expert, I want high-impact or consequential skills to require expert review and sign-off, so that the factory's own review is not mistaken for domain authority.
25. As a maintainer, I want critical evaluation failures or serious safety regressions to block a passing release, so that a strong aggregate score cannot hide a release-critical defect.
26. As a maintainer, I want the factory to generate the canonical set descriptor, human-readable overview, member skills, evaluation cases, and release evidence, so that the result is repository-ready.
27. As a maintainer, I want the factory to build and inspect a consumer archive containing the declared set contents and effective license, so that the distributed artifact matches the reviewed source.
28. As a maintainer, I want set membership and member contents pinned to an independent semantic version, so that releases are reproducible and unrelated sets can evolve separately.
29. As a maintainer, I want the factory to distinguish a draft or untested artifact from a passing release, so that missing evidence is visible and never fabricated.
30. As a skill-set owner, I want to assess change impact, rerun relevant evaluations, update versions, and deprecate or retire skills, so that the set remains trustworthy after its first release.
31. As a user whose domain knowledge may be sensitive, I want only reviewed, necessary, non-sensitive information included in packaged skills, so that discovery notes or private context are not unintentionally distributed.
32. As a maintainer, I want conditional tool-integration capabilities evaluated only through an appropriately sandboxed path, so that an untested tool-using skill is not claimed as safe or supported.

## Implementation Decisions

- Redesign the factory from first principles. Existing workflows are not binding, but useful practices may be retained when they fit the new design.
- Provide these core, focused skills:
  - `create-skill-set`: front-door coordinator, approval gates, workflow state, and handoffs; it does not duplicate phase work.
  - `discover-domain`: elicit users, tasks, terminology, constraints, edge cases, risks, sources, and uncertainty.
  - `map-skill-opportunities`: derive and prioritize skill candidates, triggers, non-triggers, boundaries, and non-goals.
  - `design-skill-set`: determine membership, responsibilities, handoffs, runtime assumptions, and conditional modules.
  - `author-skills`: create and revise portable skill instructions and supporting resources.
  - `evaluate-skills`: create evaluation cases and assess activation and task outcomes against the runtime baseline.
  - `review-safety`: perform required risk-scaled safety and security review, including expert sign-off for high-impact or consequential skills.
  - `release-skill-set`: validate the set, confirm licensing and versioning, prepare evidence, and build and inspect the consumer archive.
  - `maintain-skill-set`: assess changes, re-evaluate affected behavior, update versions and runtime evidence, and handle deprecation or retirement.
- Allow conditional specialist skills for source-intensive research, durable domain modeling, tool/script integration, or runtime-specific adaptation. Discovery must still ground important claims; conditional research is for domains requiring deeper or sustained source work.
- Keep every member skill independently useful. The coordinator guides the complete workflow, while each module has a clear responsibility and usable entry point.
- Require user approval at major scope and architecture gates before authoring or packaging. Keep user-approved choices and unresolved decisions visible throughout the workflow.
- Use the repository's canonical set descriptor, README, skill directories, per-skill evaluation cases, release report, licensing, versioning, and archive conventions. Do not add repository-specific required metadata to individual skill frontmatter.
- Keep individual skills portable by default. Document runtime-specific behavior and claim a runtime as tested only when exact runtime and model evidence exists.
- Treat structural validation and behavioral evaluation as separate requirements. Evaluation includes relevant and nearby irrelevant triggers, representative tasks, critical cases, appropriate repeats, and runtime-baseline comparison where practical.
- Never fabricate evidence. If behavioral evaluation cannot run, retain the runnable cases and mark the runtime untested or release blocked; do not emit a passing report or make a tested-runtime claim.
- Require every critical case to pass for each claimed runtime and block release on safety regressions. Tool-using conditional modules need a sandboxed evaluation path before they can be claimed as tested.
- Use an explicit effective license; follow the repository's Apache-2.0 default unless the set intentionally overrides it. Keep private discovery context out of consumer artifacts unless explicitly reviewed and approved for inclusion.
- Version each skill set independently using semantic versioning and release an exact membership/content snapshot.

## Testing Decisions

- Good behavioral tests assess externally observable activation and task outcomes, not the wording or internal organization of a skill file. Cases should use realistic prompts, include nearby irrelevant prompts, define observable rubrics, and avoid giving away the desired answer.
- Use the highest available behavioral seam: invoke the coordinator and each phase skill through the target agent runtime. Include end-to-end factory cases for intake/approval/handoff/output and independent cases for each member skill.
- Compare task cases with the same runtime baseline without the candidate set, while leaving native runtime capabilities available. Record the exact runtime, version, model, loaded skill IDs, results, and repeats.
- Keep deterministic format/repository checks separate from behavioral evaluation. Validate the canonical set and build the release archive only after the behavioral and safety gates pass; inspect archive membership and license contents.
- Test safety behavior with critical cases covering domain risk, sensitive information, unsafe tool/script behavior, and prompt-injection exposure where applicable. Verify that critical failures and safety regressions block release.
- Test maintenance behavior through representative change scenarios: skill edits, member additions/removals, runtime changes, re-evaluation, version decisions, and retirement.
- Prior art is the repository's evaluation case/report contract, runtime-baseline runner, deterministic repository checker, and release archive builder. The prior canonical skill-factory set already had fixtures for its existing skills; this feature adds cases for the new members so the complete set has coverage.
- Tool-using modules are not considered tested by ordinary skill-loading/task cases alone. They require a sandboxed evaluation seam before a tested-runtime claim is allowed.

## Out of Scope

- Creating a particular user's domain-specific skill set as part of implementing the factory itself.
- Claiming universal compatibility or automatically certifying a runtime that has not been evaluated.
- Treating source research or the factory's safety review as legal, regulatory, clinical, or other qualified professional certification.
- Building a universal sandbox for arbitrary tool integrations as a prerequisite to the core factory. Tool-integrating modules remain conditional until an appropriate sandboxed evaluation path exists.
- Publishing a set release when critical behavioral evidence or required expert sign-off is missing.

## Further Notes

- At spec creation, the skill-factory README conflicted with the descriptor and evaluation report about OpenCode testing; the implementation reconciled the README with the pending current set. The historical 0.1.0 report's generated timestamp is later than the repository's stated current date and does not cover the current complete fixture set. Tool-using workflows still require separate sandboxed evaluation before support or release claims.
- The agreed behavioral seam is coordinator end-to-end evaluation plus independent phase-skill evaluation through the real runtime, with structural validation and archive inspection as separate checks.
- The domain vocabulary in this spec follows the repository glossary: skill, skill set, set release, evaluation case, runtime baseline, and runtime matrix.
