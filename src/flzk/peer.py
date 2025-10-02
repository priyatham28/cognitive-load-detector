from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .config import Dataset, IntArray, KeyPair, TrainingConfig
from .dp_sgd import FloatArray, dp_sgd_step
from .proofs import Proof, ProofSystem


@dataclass
class LocalUpdate:
    peer_id: str
    noisy_gradient: FloatArray
    proof: Proof


class FLZKPeer:
    """Represents a single browser peer participating in FLZK."""

    def __init__(
        self,
        *,
        peer_id: str,
        dataset: Dataset,
        keypair: KeyPair,
        proof_system: ProofSystem,
        rng: np.random.Generator,
    ) -> None:
        self.peer_id = peer_id
        self._features, self._labels = dataset
        self.keypair = keypair
        self._proof_system = proof_system
        self._rng = rng
        self._model: FloatArray | None = None

    @property
    def verifying_key(self) -> str:
        return self.keypair.verifying_key

    def set_model(self, weights: FloatArray) -> None:
        self._model = weights.copy()

    def _sample_batch(self, batch_size: int) -> tuple[FloatArray, IntArray]:
        idx = self._rng.choice(self._features.shape[0], size=batch_size, replace=True)
        return self._features[idx], self._labels[idx]

    def compute_update(
        self,
        *,
        round_idx: int,
        config: TrainingConfig,
    ) -> LocalUpdate:
        if self._model is None:
            raise ValueError("Model weights must be set before training")
        batch_x, batch_y = self._sample_batch(config.batch_size)
        outcome = dp_sgd_step(
            weights=self._model,
            batch_x=batch_x,
            batch_y=batch_y,
            config=config,
            rng=self._rng,
        )
        proof = self._proof_system.prove(
            outcome=outcome,
            round_idx=round_idx,
            keypair=self.keypair,
            clip_norm=config.clip_norm,
            noise_multiplier=config.noise_multiplier,
        )
        return LocalUpdate(
            peer_id=self.peer_id,
            noisy_gradient=outcome.noisy_gradients,
            proof=proof,
        )
