---
name: author-skills
description: Design, write, or revise portable Agent Skills. Use when turning a repeatable task into a focused skill, improving a SKILL.md, or organizing its supporting scripts, references, and assets.
license: Apache-2.0
---

# Author Skills

Create one focused, portable Agent Skills directory that an agent can discover and follow reliably.

## Workflow

1. **Understand the job.** Inspect the repository and the intended users. Define the recurring task, its trigger, and an observable completion result. Ask only for missing decisions that cannot be found in the project.
2. **Set the boundary.** Keep one coherent capability in this skill. Separate work that has distinct triggers or independent outcomes into another skill. Prefer an existing shared reference over duplicating policy.
3. **Write the activation description.** Say what the skill does and when to use it. Include concrete trigger terms and adjacent cases that belong elsewhere; avoid broad claims that cause unrelated activation.
4. **Write the instructions.** Put the essential workflow in `SKILL.md`. Order steps by execution, make completion observable, and group related rules together. Keep the main file focused; move branch-specific reference, scripts, or assets into adjacent files and point to them at the step that needs them.
5. **Check portability and safety.** Use the Agent Skills frontmatter and folder conventions. Document runtime-specific behavior and environment requirements. Treat bundled scripts as executable code: inspect their inputs, side effects, dependencies, and network access.
6. **Validate and evaluate.** Run `python3 tools/check_repo.py --require-reference-validator`. Add trigger cases and task cases under the owning set's `evals/<skill-name>/cases.json`. Compare task outcomes against the same runtime baseline without the set under evaluation; preserve runtime-provided capabilities and record skills that load. Do not claim a runtime was tested without a passing report.
7. **Summarize.** Report the skill path, its trigger boundary, validation result, evaluation coverage, and any unresolved runtime or safety constraint.

## Completion criteria

- The directory name matches the `name` in `SKILL.md`.
- The description makes the capability and activation boundary clear.
- Instructions provide an ordered, usable workflow and a checkable completion result.
- Supporting files are necessary, referenced, and safe to distribute.
- Validation passes and behavioral cases cover the intended trigger and task behavior.
