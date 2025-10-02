from __future__ import annotations

from fastapi.testclient import TestClient

from src.app import app


def test_health() -> None:
    client = TestClient(app)
    response = client.get("/health")
    data = response.json()
    assert response.status_code == 200
    assert data["status"] == "ok"
    assert data["service"] == "flzk-demo"
