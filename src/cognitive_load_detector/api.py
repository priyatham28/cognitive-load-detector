from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from cognitive_load_detector import (
    CognLoadNetwork,
    MockProofSystem,
    SimulationResult,
    SnarkJSConfig,
    SnarkJSProofSystem,
    TrainingConfig,
)

app = FastAPI(title="Cognitive Load Detector — FLZK Simulator")


class SimulationRequest(BaseModel):
    rounds: int = Field(default=5, ge=1, le=200)
    num_peers: int = Field(default=5, ge=2, le=50)
    samples_per_peer: int = Field(default=128, ge=16, le=4096)
    num_features: int = Field(default=8, ge=2, le=32)
    clip_norm: float = Field(default=1.0, gt=0)
    noise_multiplier: float = Field(default=1.1, gt=0)
    learning_rate: float = Field(default=0.1, gt=0)
    batch_size: int = Field(default=32, ge=2, le=512)
    delta: float = Field(default=1e-5, gt=0)
    seed: int | None = Field(default=None)
    proof_backend: str = Field(default="mock", pattern="^(mock|snarkjs)$")


class SimulationHistory(BaseModel):
    round_idx: int
    aggregator_id: str
    accepted_updates: int
    accuracy: float
    loss: float
    epsilon: float

    @classmethod
    def from_result(cls, result: SimulationResult) -> "SimulationHistory":
        return cls(
            round_idx=result.round_idx,
            aggregator_id=result.aggregator_id,
            accepted_updates=result.accepted_updates,
            accuracy=result.accuracy,
            loss=result.loss,
            epsilon=result.epsilon,
        )


class SimulationResponse(BaseModel):
    history: list[SimulationHistory]
    final_accuracy: float
    final_loss: float
    final_epsilon: float


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "system": "cognitive_load_detector"}


def _select_proof_backend(backend: str):
    if backend == "mock":
        return MockProofSystem()
    if backend == "snarkjs":
        circuit = os.getenv("CLD_SNARKJS_CIRCUIT")
        proving_key = os.getenv("CLD_SNARKJS_PROVING_KEY")
        verification_key = os.getenv("CLD_SNARKJS_VERIFICATION_KEY")
        if not (circuit and proving_key and verification_key):
            raise HTTPException(
                status_code=400,
                detail="snarkjs backend requires CLD_SNARKJS_* environment variables",
            )
        config = SnarkJSConfig(
            circuit_path=Path(circuit),
            proving_key_path=Path(proving_key),
            verification_key_path=Path(verification_key),
        )
        try:
            return SnarkJSProofSystem(config)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
    raise HTTPException(status_code=400, detail=f"Unknown proof backend {backend}")


@app.post("/simulate", response_model=SimulationResponse)
def simulate(req: SimulationRequest) -> SimulationResponse:
    config = TrainingConfig(
        clip_norm=req.clip_norm,
        noise_multiplier=req.noise_multiplier,
        learning_rate=req.learning_rate,
        batch_size=req.batch_size,
        delta=req.delta,
    )
    proof_system = _select_proof_backend(req.proof_backend)
    network = CognLoadNetwork(
        num_peers=req.num_peers,
        samples_per_peer=req.samples_per_peer,
        num_features=req.num_features,
        config=config,
        seed=req.seed,
        proof_system=proof_system,
    )
    history = [SimulationHistory.from_result(r) for r in network.simulate(req.rounds)]
    final = history[-1]
    return SimulationResponse(
        history=history,
        final_accuracy=final.accuracy,
        final_loss=final.loss,
        final_epsilon=final.epsilon,
    )
