---
name: runtime-adaptation
description: Adapt a portable Agent Skills design for a named agent runtime, document verified runtime-specific differences, or assess evidence for runtime support claims; do not infer compatibility from format checks or another runtime's results.
license: Apache-2.0
---

# Adapt and Validate Runtime Support

Use this skill conditionally when a skill or set has a concrete requirement for a named runtime, when documenting differences between runtimes, or when deciding whether evaluation evidence supports a runtime claim. Keep portable Agent Skills behavior as the default; this skill does not make runtime-specific adaptation mandatory for every set.

## Workflow

1. **Establish the scope.** Identify the skill or set, intended users, named target runtimes, and the concrete need for adaptation. Separate the user's goals from assumptions. If no runtime-specific need exists, recommend keeping the portable design and do not add this capability speculatively.
2. **Start with the portable design.** Preserve the Agent Skills structure and instructions as the shared behavior. Identify the smallest runtime-specific difference needed, and keep it isolated and optional where possible. Do not weaken the portable path to accommodate an undocumented runtime quirk.
3. **Ground each difference.** For each named runtime, record the actual requirement or behavior, its source (such as runtime documentation or a supplied observed result), and its effect on skill layout, discovery, instructions, or use. Distinguish verified facts from user-provided assumptions and unknowns. If evidence is missing, ask for it or label the detail unresolved; do not invent runtime conventions, APIs, configuration, or capabilities.
4. **Choose the runtime matrix.** List only runtimes intentionally targeted. Keep target status separate from tested status. Define the evaluation cases and completion criteria needed for each target; cover the skill's relevant behavior and important runtime-specific differences. A runtime absent from the evaluator remains unsupported or unevaluated, not implicitly compatible.
5. **Assess evidence independently per runtime.** A tested claim requires completed, passing behavioral results for that exact runtime version and model, covering the authored cases and required repeats, with the results and limitations recorded in the set's evaluation report. A format validator, static check, proposed plan, partial run, or another runtime's passing result is not behavioral evidence for the target runtime.
6. **Make a precise decision.** Report each runtime as target/untested, unsupported, or tested only when its evidence satisfies the set's evaluation and release gates. State the exact scope of any supported claim and material limitations. Keep missing or conflicting evidence visible; request evaluation or documentation rather than filling gaps with estimates.

## Runtime difference record

For each difference that affects the delivered skill, record:

- **Runtime and scope:** exact runtime name and the skill/set behavior affected.
- **Difference and source:** the requirement or observed behavior, with its documentation or evidence source and version when available.
- **Portable path:** what remains standard Agent Skills behavior and whether a separate runtime-specific file, instruction, or packaging step is actually necessary.
- **Status and limits:** verified, user-provided but unverified, or unresolved; include implications for evaluation and support claims.

Do not turn a runtime-specific note into a universal requirement. Do not claim “works everywhere” or equivalent universal support.

## Output shape

Adapt this outline to the available evidence. Use “unknown,” “not evaluated,” or “not provided” instead of guessing.

```markdown
# Runtime adaptation: <skill or set>

## Portable behavior
## Concrete adaptation need
## Runtime differences and sources
## Target runtime matrix
| Runtime | Target? | Exact version/model evidence | Evaluation status | Limits |
## Missing evidence and next steps
## Support decision
```

## Boundaries

- Do not add runtime-specific behavior without a concrete need tied to a named runtime.
- Do not treat a declared target, successful format check, or one runtime's result as evidence that another runtime works.
- Do not mark a runtime tested without complete, passing behavioral evidence for that runtime and exact identity details.
- Do not fabricate versions, model identifiers, documentation, evaluation results, or compatibility guarantees.
- Do not claim universal compatibility. Describe only the runtimes and behaviors supported by the available evidence.

## Completion check

The adaptation is reviewable when portable behavior remains the default, each runtime-specific difference is documented with its source and status, targets are distinguished from tested runtimes, and support claims are no broader than completed evidence. Otherwise, leave the decision untested and list the evidence needed next.
