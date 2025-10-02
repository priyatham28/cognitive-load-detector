from __future__ import annotations

from fastapi.testclient import TestClient

from src.app import app


def test_simulate_defaults() -> None:
    client = TestClient(app)
    response = client.post("/simulate", json={"rounds": 2})
    body = response.json()

    assert response.status_code == 200
    assert body["rounds"] == 2
    assert len(body["metrics"]) == 2
    assert body["metrics"][0]["acc"] < body["metrics"][1]["acc"]
    assert body["privacy"]["eps"] > 0
