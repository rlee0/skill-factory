# Contributing

Contributions are welcome through pull requests.

## Before opening a pull request

- Keep each skill focused on one capability and follow the Agent Skills format.
- Add or update trigger and task evaluation cases for changed behavior.
- Run `python3 tools/check_repo.py --require-reference-validator`.
- Review bundled scripts and resources for safety, licensing, and unnecessary dependencies.
- When OpenCode and its API credential are available, set `OPENCODE_API_KEY` in the shell or ignored `.env`, then run `python3 tools/run_evaluations.py <set> --model <provider/model>` and review outputs against the case rubrics.

Behavioral evaluations use model credentials and must run only in an approved environment. Fork pull requests require a maintainer-triggered run. Never place credentials or private user data in skills, test cases, reports, or raw trace artifacts.

## Review and release

One maintainer approval is the initial release-candidate review bar. Public releases are per set, use SemVer, and require passing critical scenarios on every claimed runtime. Maintainers publish draft releases only after inspecting the archive and report.
