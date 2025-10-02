# Repository Audit Summary

## Identity
- **Chosen scope:** FLZK (verifiable browser-based federated learning) aligned
  with the original research artefact.

## Highlights
- Added a typed simulation core (`flzk.simulation`) with docstrings and TODOs
  for future engineering work.
- Replaced the FastAPI entry point with a clean, typed façade that exercises the
  simulator and surfaces realistic metadata.
- Pinned dependencies in `pyproject.toml`, introduced optional `dev` extras, and
  simplified `requirements.txt` to use them.
- Expanded documentation: professional README, CONTRIBUTING, Code of Conduct,
  issue templates, and a Jupyter notebook walkthrough.
- Upgraded tests to cover the simulator, package metadata, and API contracts
  while maintaining 100% coverage.
- Polished CI, developer tooling, and repository hygiene (.gitignore, badges,
  notebook, TODO markers).

## Reproduction commands
- `make setup` — create virtual environment and install deps.
- `make run` — launch FastAPI server.
- `make demo` — open Streamlit dashboard.
- `make test` — run lint, type checking, and pytest with coverage.
- `make build` — produce sdist/wheel artifacts.

## CI
GitHub Actions workflow: `.github/workflows/ci.yml` (Python 3.10 & 3.11). Includes
linting, typing, tests, packaging, and API smoke check.
