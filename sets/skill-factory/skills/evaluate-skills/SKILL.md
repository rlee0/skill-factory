---
name: evaluate-skills
description: Design or review evaluations for agent skills. Use when checking skill activation, comparing task outcomes against a runtime baseline without the candidate set, defining critical scenarios, or recording runtime and model evidence.
license: Apache-2.0
---

# Evaluate Skills

Build evidence for whether a skill activates in the right situations and improves the work an agent does.

## Workflow

1. **Identify the claim.** State what the skill should help with, when it should activate, and which user-visible outcome should improve. Keep format validity separate from effectiveness.
2. **Choose representative cases.** Add relevant trigger prompts, nearby irrelevant prompts, and realistic task prompts. Include edge cases that would expose unsafe actions or incorrect assumptions.
3. **Write observable criteria.** For each task, define specific success criteria and mark whether failure is release-critical. Prefer checks against outputs or traces over judging whether the instructions merely look plausible.
4. **Set the comparison.** Compare the skill-enabled run with the same runtime baseline for the task. Keep runtime-provided capabilities constant and remove the skill set under evaluation from the baseline. Keep the model, task inputs, and rubric comparable; explain any difference that cannot be controlled.
5. **Set repetitions.** Choose repeat counts per case based on risk and variability. Critical cases must pass every required run; an aggregate score cannot hide a critical failure.
6. **Run on claimed runtimes.** Record the exact runtime and model versions. Treat each runtime independently. Report untested runtimes as targets, never as verified compatibility.
7. **Record results.** Save a report at `sets/<set>/reports/<version>.json`. Include case-level outcomes, repeats, failures, safety regressions, and limitations. Do not expose credentials, private data, or raw sensitive traces.
8. **Make the decision.** A release is blocked by a critical failure or serious safety regression. Explain non-critical failures and any limits on the claim.

## Completion criteria

- The case suite covers activation and task outcomes for the intended boundary.
- Baselines and comparison conditions are stated.
- Criticality and repeat counts are explicit.
- Results identify exact runtimes and models and satisfy the set's release gate.
- The report supports the compatibility claim without overstating it.
