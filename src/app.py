from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from flzk import SimulationConfig, run_simulation

app = FastAPI(title="FLZK Demo API", version="0.1.0")


class SimRequest(BaseModel):
    """Validated payload for /simulate requests."""

    rounds: int = 5
    num_peers: int = 4
    samples_per_peer: int = 256
    clip_norm: float = 1.0
    noise_multiplier: float = 1.1
    learning_rate: float = 0.1
    batch_size: int = 32
    num_features: int = 8
    proof_backend: str = "mock"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "flzk-demo"}


@app.post("/simulate")
def simulate(req: SimRequest) -> dict[str, object]:
    config = SimulationConfig(
        rounds=req.rounds,
        num_peers=req.num_peers,
        samples_per_peer=req.samples_per_peer,
        clip_norm=req.clip_norm,
        noise_multiplier=req.noise_multiplier,
        learning_rate=req.learning_rate,
        batch_size=req.batch_size,
        num_features=req.num_features,
    )
    summary = run_simulation(config, backend=req.proof_backend)
    return {
        "rounds": req.rounds,
        "num_peers": req.num_peers,
        "metrics": [
            {"round": metric.round, "acc": metric.accuracy, "loss": metric.loss}
            for metric in summary.metrics
        ],
        "privacy": {"eps": summary.epsilon, "delta": summary.delta},
        "backend": summary.backend,
    }
