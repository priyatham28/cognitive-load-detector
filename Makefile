.PHONY: setup run demo test lint type format docker build

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt

run:
	python -m uvicorn cognitive_load_detector.api:app --host 0.0.0.0 --port 8000

demo:
	streamlit run demo/streamlit_app.py

test:
	pytest

lint:
	ruff check .

type:
	mypy src

format:
	ruff format .

build:
	python -m build

docker:
	docker build -t cognitive-load-detector:latest .
