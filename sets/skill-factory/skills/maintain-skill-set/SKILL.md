---
name: maintain-skill-set
description: "Assess proposed changes to an already released agent skill set: map impact, plan re-evaluation, recommend independent SemVer, maintain runtime evidence, or deprecate/retire skills. Use for maintenance planning before a release candidate is ready; not for validating a candidate's release readiness (use release-skill-set)."
license: Apache-2.0
---

# Maintain a Skill Set

Keep a released skill set trustworthy as its contents and operating context change. Work from the exact released snapshot and proposed changes; produce a traceable maintenance plan, not unearned evidence or release claims.

## Workflow

1. **Fix the baseline.** Identify the set, current version, released revision or archive, current descriptor and overview, proposed revision, and the owner's requested outcome. Read the set's release and evaluation policy when available. If the released snapshot or proposed change is unclear, ask for it; do not infer what changed from a version label.
2. **Map impact.** Compare the exact current and proposed contents. For every change, record affected member skills, triggers and boundaries, evaluation cases, source assumptions, safety/security findings, tool or script behavior, runtime-specific instructions, set membership, user documentation, license, and compatibility claims. Mark each item as affected, unaffected with a reason, or unknown. Include downstream users and workflows where known. Treat changes to a source, domain, runtime, or dependency as potential impacts even when the skill text is unchanged.
3. **Choose review and evaluation.** For each affected behavior, identify the cases and other evidence that need review or rerun. Re-evaluate changed and impacted skills on each runtime for which support is claimed, using the same runtime baseline without the candidate set while retaining native runtime capabilities. Preserve exact runtime version, model, cases, repeats, loaded-skill observations, and task baselines as required by the evaluation protocol. Revisit safety review, expert sign-off, or sandbox evidence when the changed content or behavior affects those gates. If a runtime is unsupported or evidence is incomplete, leave it untested or pending; never infer a pass from old results, another runtime, or a structural check.
4. **Recommend the set's SemVer independently.** Apply the set's user-visible compatibility policy to the exact proposed membership and behavior: a breaking behavior change or member removal is major; a compatible capability or member addition is minor; a correction that does not change intended behavior is patch. When changes of several kinds are combined, recommend the highest applicable change. Do not bump unrelated sets or a repository-wide version. Keep the descriptor and human-readable version consistent. Preserve historical reports; new or changed sources need evidence for their exact version before new claims are made.
5. **Plan lifecycle changes.** For a skill proposed for deprecation or retirement, record why, affected users, risks of continued use, replacement or migration path, communication, transition timing, and owner approval needed. Prefer a clear deprecation period where continued use is safe and useful; when a safety or security issue makes continued use unacceptable, recommend an appropriately urgent retirement and direct users to a safe alternative. Removal changes exact set membership and is a breaking change. Update the descriptor, overview, local discovery links if present, affected fixtures, and migration guidance together. Keep prior released snapshots and reports as historical records.
6. **Hand off an exact candidate.** Summarize changes and owners, evidence to rerun, review gates, proposed independent version, membership/document updates, unresolved decisions, and what remains pending or untested. Make clear that a plan is not completed evaluation, approval, tag, archive, or release. Only perform file changes or release actions the user explicitly authorized; otherwise provide the proposed patch or handoff.

## Boundaries

- This skill starts from an existing release and can be used without the original set-creation workflow.
- Repository release policy takes precedence for that repository. For another set, identify its own compatibility policy; if none exists or the SemVer impact is ambiguous, state the assumption and ask the owner rather than silently imposing repository-specific rules.
- Treat every runtime separately. A runtime target is not a tested-runtime claim; only complete, reviewed evidence for the exact runtime version and model supports that claim.
- Keep evaluation results, safety reviews, expert sign-off, and sandbox evidence distinct. One cannot substitute for another.
- Do not overwrite old release evidence, fabricate results, or present a proposed maintenance plan as a completed change.

## Completion criteria

The handoff accounts for every proposed change and affected artifact; names the evaluations and independent review gates still needed; recommends a version with its compatibility rationale; describes any user-facing deprecation or retirement path; and labels unresolved, pending, and untested items explicitly.
