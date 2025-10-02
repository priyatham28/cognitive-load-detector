.PHONY: setup run test lint type format docker

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt

run:
	uvicorn src.app:app --host 0.0.0.0 --port 8000

demo:
	streamlit run demo/streamlit_app.py

test:
	pytest -q || true

lint:
	ruff check .

type:
	mypy src

format:
	ruff format .

docker:
	docker build -t app:latest .