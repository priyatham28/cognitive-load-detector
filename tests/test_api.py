from __future__ import annotations

from fastapi.testclient import TestClient

from cognitive_load_detector.api import app


def test_simulate_endpoint_roundtrip() -> None:
    client = TestClient(app)

    payload = {
        "rounds": 2,
        "num_peers": 3,
        "samples_per_peer": 64,
        "num_features": 4,
        "clip_norm": 1.0,
        "noise_multiplier": 1.0,
        "learning_rate": 0.1,
        "batch_size": 16,
        "proof_backend": "mock",
    }

    response = client.post("/simulate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["final_accuracy"] >= 0.0
    assert len(body["history"]) == payload["rounds"]


def test_health_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["system"] == "cognitive_load_detector"
