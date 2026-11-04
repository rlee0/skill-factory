# Evaluation protocol

Evaluation separates structural validity from observed behavior. Passing a format validator does not prove that a skill is effective.

## Case design

Each skill owns `skills/<skill-name>/evals/cases.json`. Include:

- **Trigger cases**: relevant prompts that should activate the skill and nearby irrelevant prompts that should not.
- **Task cases**: representative tasks with observable success criteria.
- **Baseline**: compare the task with the skill available against the same task without it where practical.
- **Criticality and repeats**: mark release-critical cases and set repeat counts per case. Any critical failure or serious safety regression blocks release.
- **Task comparison**: task cases set `comparison_policy` to `uplift` or `no-regression`; CI compares criterion scores against the runtime baseline.

Use realistic, safe prompts. Keep the task and rubric in the case file; do not encode a desired answer in a prompt in a way that gives the skill the answer.

## Runtime evidence

Evaluate each runtime a set claims as tested. Record the runtime version, model identifier, case results, repeats, and overall status in `reports/<version>.json`. Model choices may vary, but every result must identify the exact model used. Never infer compatibility for an untested runtime. For a concrete runtime-specific requirement, document the difference and its source while keeping portable Agent Skills behavior as the default; target status, format validation, and evidence from another runtime do not establish tested support.

The pilot currently targets OpenCode, but `tested_runtimes` remains empty until complete evidence is reviewed. The checked-in v0.1.0 report has a generated timestamp later than the repository's current date and does not cover the current complete fixture set; it is not evidence for the current sources or a release claim. The local runner retains traces for manual review; CI emits sanitized case scores and repeat-level skill observations while raw traces remain in temporary workspaces. Behavioral CI runs affected skills with `opencode/gpt-6-luna`; update runtime claims and release reports only after reviewing complete evidence.

Set `OPENCODE_API_KEY` in the local environment or in the ignored repository-root `.env` file, then run critical cases once each with `--smoke`. A shell variable takes precedence over `.env`:

```sh
.venv/bin/python tools/run_evaluations.py skill-factory --model opencode/gpt-6-luna --smoke
```

The harness launches each run in a fresh temporary workspace and passes only `OPENCODE_API_KEY` to the CLI. All actions except skill loading are denied for task runs; the separate rubric judge has all tools denied. The treatment installs the pilot set; the runtime baseline omits it while retaining OpenCode-provided skills. Manifests record both set skills installed and skill IDs actually loaded, so native skills remain visible in the comparison. This measures the set's added value over the runtime users have. A relevant trigger passes only when its expected skill loads; an irrelevant trigger passes only when that target skill does not load. In CI, the judge returns one boolean per criterion plus a serious-safety-regression decision. The treatment must satisfy every criterion; `uplift` additionally requires a higher criterion count than baseline, while `no-regression` allows an equal count. Raw local output and manifests are written under ignored `evaluation-runs/`; review them locally and do not commit them.

`--smoke` runs every critical case once: one treatment run for triggers, and paired treatment/baseline runs for tasks. The number of CLI runs depends on the checked-in cases. If a run errors, evidence is missing, or any critical case fails, review the runner or skill and repeat the smoke before running the full suite. Manually score against each case's criteria. The local harness leaves results at `pending-human-review`; a maintainer records the passing release report only after complete review. Tool-using skill evaluations need a separate sandboxed runner.

## Pull requests and releases

Run deterministic checks on every pull request. After `Checks` succeeds, `Behavioral Evaluations` evaluates only changed skills from trusted default-branch runner code; candidate files are checked out separately and treated as data. The `skill-evaluations` GitHub Environment gates the API key behind required reviewer approval. Fork pull requests do not run automatically; a maintainer can dispatch the workflow with an open PR number. Raw traces are never uploaded or written to job logs; only sanitized case statuses and counts appear in the job summary. Critical rubric failures, runtime errors, or activation errors fail the check; non-critical rubric failures are reported but do not block it.

Before release, every critical case must pass for every claimed runtime. A good aggregate score cannot cancel a critical failure. Attach the passing report to the draft release and keep case fixtures in tagged source, not in the consumer archive.

## Report contract

Reports are JSON with `set`, `version`, `status`, `generated_at`, and a `runtimes` array. Every runtime entry records `name`, `version`, `model`, `status`, and case results. A release report must have `status: "passed"`; each target runtime must have a passing entry. The `tools/build_set.py --for-release` command enforces this contract.

Each runtime's `cases` array must include every authored case. Each case result records its `id`, `status` (`passed` or `failed`), `critical` flag, `safety_regression` boolean, `expected_activation`, `runs_with_target_skill`, the observed `loaded_skill_ids`, and completed `repeats`. `run_evidence` must contain one record per repeat with treatment status, observed loaded skill IDs, activation result, every criterion score, and safety result. Task cases also record paired `baseline_repeats`, `baseline_loaded_skill_ids`, and per-repeat baseline status, loaded IDs, and criterion scores. Summary fields must agree with the repeat records. Runtime version and exact model identifier are required; the runtime baseline must retain native capabilities while omitting the candidate set.

Missing identity, response/trace, activation observations, repeats, rubric scores, or task baseline evidence is incomplete evidence—not a negative result and never a pass. Unsupported runtimes remain untested. A failed non-critical case needs a rationale. Any safety regression blocks release, as does any critical failure.
