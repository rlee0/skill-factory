---
name: evaluate-skills
description: Design or review behavioral evaluations and runtime evidence for agent skills. Use when asked to assess skill activation or task outcomes, compare runs against a runtime baseline, or plan or record evaluation results. Do not use for editing skill documentation, evaluation policy, or case wording unless behavioral evaluation is also requested; use author-skills for skill documentation.
license: Apache-2.0
---

# Evaluate Skills

Build evidence for whether a skill activates in the right situations and improves the work an agent does.

## Workflow

1. **Identify the claim.** State what the skill should help with, when it should activate, and which user-visible outcome should improve. Keep format validity separate from effectiveness.
2. **Choose representative cases.** Add relevant trigger prompts, nearby irrelevant prompts, and realistic task prompts. Include edge cases that would expose unsafe actions or incorrect assumptions.
3. **Write observable criteria.** For each task, define specific success criteria and mark whether failure is release-critical. Prefer checks against outputs or traces over judging whether the instructions merely look plausible.
4. **Set the comparison.** Compare the skill-enabled run with the same runtime baseline for the task. Keep runtime-provided capabilities constant and remove the skill set under evaluation from the baseline. Keep the model, task inputs, and rubric comparable; explain any difference that cannot be controlled.
5. **Set repetitions.** Choose repeat counts per case based on risk and variability. Critical cases must pass every required run; an aggregate score cannot hide a critical failure. Any serious safety regression blocks release regardless of criticality or aggregate score.
6. **Run on claimed runtimes.** Record the exact runtime version and model identifier. Treat each runtime independently. Report unsupported or untested runtimes as untested, never as verified compatibility.
7. **Record results.** Save a report at `sets/<set>/reports/<version>.json`. Include every authored case, per-repeat treatment and baseline status, criterion scores, observed loaded skill IDs, failures, safety regressions, and limitations. Do not expose credentials, private data, or raw sensitive traces.
8. **Make the decision.** A release is blocked by a critical failure or serious safety regression. Explain non-critical failures and any limits on the claim.

## Missing evidence

- Missing runtime/model identity, response/trace, loaded-skill observations, repeats, or task baseline evidence makes the affected result incomplete. When proposing a rerun, explicitly request the full authored case suite (relevant and nearby-irrelevant triggers and tasks), required repeats, treatment/baseline outputs and loaded-skill IDs, and exact runtime/model identity. The task baseline keeps native runtime capabilities while omitting only the candidate set. Do not interpret absent observations as a negative activation or a passing outcome.
- A format check is not behavioral evidence. Do not fill gaps with inferred values, prior runs, or another runtime's result.
- Keep the set pending/untested until the evidence is complete. A runtime the runner does not support remains untested; do not create a passing report for it.
- Do not treat editing evaluation-related prose or fixtures as a request to assess behavior; hand off bounded skill-documentation edits to `author-skills` unless evaluation is also requested.

## Completion criteria

- The case suite covers activation and task outcomes for the intended boundary.
- Baselines and comparison conditions are stated.
- Criticality and repeat counts are explicit.
- Results identify exact runtimes and models and satisfy the set's release gate.
- The report supports the compatibility claim without overstating it.
