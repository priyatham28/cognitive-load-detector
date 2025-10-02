.PHONY: setup run demo test format lint type build security release-notes

PY ?= python

setup:
	$(PY) -m venv .venv
	. .venv/bin/activate; pip install -U pip
	. .venv/bin/activate; pip install -e .
	. .venv/bin/activate; pip install -r requirements.txt || true
	. .venv/bin/activate; pip install ruff mypy pytest pytest-cov build httpx uvicorn bandit pip-audit pre-commit

run:
	. .venv/bin/activate; uvicorn src.app:app --host 127.0.0.1 --port 8000

demo:
	. .venv/bin/activate; streamlit run demo/streamlit_app.py

test:
	. .venv/bin/activate; ruff check .
	. .venv/bin/activate; mypy src || true
	. .venv/bin/activate; pytest -q --disable-warnings --maxfail=1 --cov=src --cov-report=term-missing

format:
	. .venv/bin/activate; ruff format .

lint:
	. .venv/bin/activate; ruff check .

type:
	. .venv/bin/activate; mypy src

build:
	. .venv/bin/activate; python -m build

security:
	. .venv/bin/activate; bandit -q -r src
	. .venv/bin/activate; pip install -U setuptools >/dev/null
	. .venv/bin/activate; pip-audit --progress-spinner off -r requirements-app.txt --ignore-vuln GHSA-4xh5-x5gv-qwph

release-notes:
	@echo "## Release Notes"
	@python scripts/generate_release_notes.py
