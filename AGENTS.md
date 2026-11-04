## Agent skills

### Skill sets

- Repository purpose, setup, and commands: `README.md`
- Set structure and authoring rules: `docs/skill-sets.md`
- Evaluation protocol: `docs/evaluation.md`
- Release protocol: `docs/releases.md`
- First-party set: `sets/skill-factory/`

Run `python3 tools/check_repo.py` after changing a set or its skills. Use `python3 tools/build_set.py --help` to build a consumer archive.

### Issue tracker

Issues and specs live as markdown files under `.scratch/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the default labels: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: root `GLOSSARY.md` and `docs/adr/`. See `docs/agents/domain.md`.
