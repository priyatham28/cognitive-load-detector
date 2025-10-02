# Cognitive Load / Meeting Fatigue Detector (Real‑Time, Multimodal)

Detect high cognitive load / fatigue in online meetings using **video, audio, and interaction** signals. Optimized for **on‑device** CPU inference.

## Quickstart
```bash
make setup
make run        # FastAPI on :8000
make demo       # Streamlit demo
```

## API
- `GET /health` → `{status: "ok"}`
- `POST /infer` → `{load_score, confidence}`

## Repo Health
CI checks lint, types, tests, and a smoke server.