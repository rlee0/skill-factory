# Skill sets

## Source layout

Each set owns its source directory:

```text
sets/<set-name>/
├── set.json
├── README.md
└── skills/<skill-name>/
    ├── SKILL.md
    └── evals/cases.json
```

Each skill owns its `evals/cases.json` alongside `SKILL.md` and optional `scripts/`, `references/`, and `assets/`. Skills use the Agent Skills specification. Set metadata belongs in `set.json`; do not add repository-specific required fields to every skill's frontmatter.

The first-party pilot is linked into `.agents/skills/` for local OpenCode discovery. The set directory remains canonical, and release archives contain real skill files rather than symlinks.

Skills should remain useful independently. When multiple sets genuinely need the same skill, introduce one explicit shared source and reference it from each set; do not maintain divergent copies.

## Set descriptor

`set.json` is the machine-readable catalog entry. It records the set name, current source version, purpose, license, exact member paths, target runtimes, tested runtimes, and evaluation status. `tested_runtimes` is evidence, not an aspiration: leave it empty until successful behavioral results exist for that runtime.

The set README is the human-readable overview. Set names and skill names use lowercase kebab-case. Each skill directory name must match its Agent Skills `name` field.

## Compatibility and licensing

Sets target portable Agent Skills directories. Runtime-specific behavior is allowed only when documented. State a runtime as tested only when its exact version and model are recorded in a passing evaluation report.

Apache-2.0 is the default set license. A set may override it by bundling a set-local `LICENSE`. A skill may override the set default by naming a license file bundled inside that skill directory. The effective license must be explicit before public release; the consumer archive includes the set license and all member skill files.
