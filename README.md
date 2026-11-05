# Skill Factory

A public, reusable workshop for developing, evaluating, safety-reviewing, and shipping curated sets of portable agent skills. The repository also maintains the `skill-factory` set as its first-party pilot.

## Repository model

- A **skill** is an [Agent Skills](https://agentskills.io/specification) directory with a `SKILL.md` and optional resources.
- A **skill set** is a curated collection of independently usable skills with its own descriptor, compatibility claims, evaluation evidence, and release version.
- Set sources live under `sets/<set-name>/`. Each set owns its skills and evaluation cases. Shared skill sources are introduced only when reuse is real.
- Releases are set snapshots. A set's SemVer changes independently of other sets.

See [`GLOSSARY.md`](GLOSSARY.md), [set conventions](docs/skill-sets.md), [evaluation](docs/evaluation.md), and [releases](docs/releases.md).

## First-party pilot

[`sets/skill-factory/`](sets/skill-factory/) contains thirteen focused skills:

- `author-skills` — author or revise a portable skill from an approved design, independently of the coordinator.
- `create-skill-set` — coordinate the factory workflow, approval gates, and phase handoffs.
- `design-skill-set` — define tailored set membership, responsibilities, handoffs, and runtime assumptions.
- `discover-domain` — elicit and review domain context.
- `domain-modeling` — clarify shared domain language and record consequential decisions.
- `evaluate-skills` — define and assess activation and task outcomes.
- `integrate-tools-safely` — design authorized tool/script integrations with least privilege and sandboxed evaluation gates.
- `map-skill-opportunities` — derive and prioritize bounded skill candidates.
- `maintain-skill-set` — assess post-release changes, evidence, versioning, deprecation, and retirement.
- `research-domain` — deepen a domain brief with focused, trustworthy sources.
- `release-skill-set` — prepare a versioned set release.
- `runtime-adaptation` — conditionally document named runtime differences and assess runtime support evidence.
- `review-safety` — review safety and security risks, require expert sign-off for consequential use, and enforce release gates.

The `0.3.0` pilot's behavioral evaluation passed for OpenCode; see the [versioned report](sets/skill-factory/reports/0.3.0.json). The set is not yet released and awaits maintainer review of the exact report and archive; see the [safety review](docs/reviews/skill-factory-0.3.0-safety-review.md). The checked-in `0.1.0` report is historical and does not cover the current complete fixture set. Repository checks compare tested-runtime claims with the report for the exact set version, but do not establish report provenance or replace release gates. See the [evaluation protocol](docs/evaluation.md).

The pilot skills are linked into `.agents/skills/` for local OpenCode discovery. Set sources remain canonical under `sets/skill-factory/`.

## Additional sets

- [`home-assistant`](sets/home-assistant/README.md) — eight cautious Home Assistant skills; draft, evaluation pending, no tested runtimes.
- [`monarch-money`](sets/monarch-money/README.md) — eight Monarch Money skills; draft, evaluation pending, no tested runtimes. The packaged glossary contains only general terms, not household-specific settings.

## Quick start

Python 3.11 or newer is required for repository checks and archive builds.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python tools/check_repo.py --require-reference-validator
.venv/bin/python tools/build_set.py skill-factory --output dist
```

For local OpenCode evaluations, copy `.env.example` to `.env` and set `OPENCODE_API_KEY`. `.env` is ignored by Git; an `OPENCODE_API_KEY` already set in the shell takes precedence.

`skills-ref` is the Agent Skills project's reference validator, not a production-supported package. The development requirement pins its source to an official repository commit; it does not install the similarly named PyPI distribution.

## Contribute

Open a pull request for changes. Static checks validate set descriptors, evaluation-case structure, and every skill. Behavioral evaluation runs after static checks for affected skills; fork PRs require a maintainer-triggered run. Behavioral release evidence is still required before release; see [the evaluation protocol](docs/evaluation.md).

## License

Unless a set declares an override, repository content is licensed under [Apache-2.0](LICENSE). A set archive includes the applicable license.
