# Contributing to FLZK Demo

Thanks for considering a contribution! This repository is intentionally small,
so a little polish goes a long way.

## Getting started
1. Fork the repository and create a feature branch: `git checkout -b feature/<slug>`.
2. Install dependencies: `make setup`.
3. Run the test suite and linters before pushing: `make test`.

## Coding guidelines
- **Type hints:** All new functions should include type annotations.
- **Docstrings:** Provide intent-focused docstrings for public functions and
  modules.
- **Tests:** Each change should have a corresponding unit test. Coverage checks
  run via GitHub Actions.
- **Style:** We use `ruff` for linting/formatting. Run `make lint` before opening
  a pull request.
- **Commit messages:** Follow the pattern `scope: short description`, e.g.
  `sim: support configurable noise multiplier`.

## Pull request checklist
- [ ] Tests added or updated.
- [ ] `make lint` and `make test` pass locally.
- [ ] README or docs updated if behaviour changes.
- [ ] Added realistic TODOs when appropriate (avoid generic "TODO" without
      context).

## Reporting issues
File bugs via the GitHub issue templates. When in doubt include reproduction
steps, expected/actual behaviour, and environment details.

Happy hacking!
