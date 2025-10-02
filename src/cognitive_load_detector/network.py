from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import List

import numpy as np

from .config import TrainingConfig
from .dataset import generate_synthetic_dataset
from .dp_sgd import FloatArray, apply_update, logistic_accuracy, logistic_loss
from .peer import CognitiveLoadPeer
from .proofs import MockProofSystem, ProofSystem
from .privacy import approximate_epsilon

LOGGER = logging.getLogger("cognitive_load_detector.network")


@dataclass
class SimulationResult:
    round_idx: int
    aggregator_id: str
    accepted_updates: int
    accuracy: float
    loss: float
    epsilon: float


class CognitiveLoadNetwork:
    """Simulated peer-to-peer training loop."""

    def __init__(
        self,
        *,
        num_peers: int,
        samples_per_peer: int,
        num_features: int,
        config: TrainingConfig,
        seed: int | None = None,
        proof_system: ProofSystem | None = None,
    ) -> None:
        self.config = config
        self._rng = np.random.default_rng(seed)
        self._samples_per_peer = samples_per_peer
        model_dim = num_features + 1  # bias term
        self._global_model: FloatArray = np.zeros(model_dim, dtype=float)
        self._proof_system = proof_system or MockProofSystem()
        self._peers: list[CognitiveLoadPeer] = []
        self._verifying_keys: dict[str, str] = {}
        for peer_idx in range(num_peers):
            dataset = generate_synthetic_dataset(
                num_samples=samples_per_peer,
                num_features=num_features,
                rng=self._rng,
            )
            key_seed = f"peer-{peer_idx}-{self._rng.integers(0, 2**32)}"
            keypair = self._proof_system.generate_keypair(key_seed)
            peer_rng = np.random.default_rng(self._rng.integers(0, 2**32))
            peer = CognitiveLoadPeer(
                peer_id=f"peer-{peer_idx}",
                dataset=dataset,
                keypair=keypair,
                proof_system=self._proof_system,
                rng=peer_rng,
            )
            peer.set_model(self._global_model)
            self._peers.append(peer)
            self._verifying_keys[peer.peer_id] = peer.verifying_key
        eval_ds = generate_synthetic_dataset(
            num_samples=2048,
            num_features=num_features,
            rng=self._rng,
        )
        self._eval_features, self._eval_labels = eval_ds
        self._round = 0

    @property
    def peers(self) -> List[CognitiveLoadPeer]:
        return self._peers

    def _broadcast_model(self, model: FloatArray) -> None:
        for peer in self._peers:
            peer.set_model(model)

    def run_round(self) -> SimulationResult:
        if not self._peers:
            raise RuntimeError("No peers registered")
        aggregator_idx = int(self._rng.integers(0, len(self._peers)))
        aggregator = self._peers[aggregator_idx]
        LOGGER.debug("Round %s aggregator=%s", self._round, aggregator.peer_id)

        updates = [peer.compute_update(round_idx=self._round, config=self.config) for peer in self._peers]

        accepted: list[FloatArray] = []
        for update in updates:
            proof = update.proof
            verifying_key = self._verifying_keys[update.peer_id]
            if abs(proof.clip_norm - self.config.clip_norm) > 1e-6:
                LOGGER.debug("Rejecting %s: clip norm mismatch", update.peer_id)
                continue
            if abs(proof.noise_multiplier - self.config.noise_multiplier) > 1e-6:
                LOGGER.debug("Rejecting %s: noise multiplier mismatch", update.peer_id)
                continue
            if self._proof_system.verify(
                noisy_gradient=update.noisy_gradient,
                proof=proof,
                verifying_key=verifying_key,
            ):
                accepted.append(update.noisy_gradient)
            else:
                LOGGER.debug("Proof verification failed for %s", update.peer_id)

        if not accepted:
            LOGGER.warning("No valid updates in round %s; inserting zero vector", self._round)
            accepted.append(np.zeros_like(self._global_model))

        avg_grad = np.mean(accepted, axis=0)
        self._global_model = apply_update(
            self._global_model,
            avg_grad,
            learning_rate=self.config.learning_rate,
        )
        self._broadcast_model(self._global_model)

        self._round += 1
        rounds_completed = self._round
        accuracy = logistic_accuracy(self._global_model, self._eval_features, self._eval_labels)
        loss = logistic_loss(self._global_model, self._eval_features, self._eval_labels)
        epsilon = approximate_epsilon(
            noise_multiplier=self.config.noise_multiplier,
            batch_size=self.config.batch_size,
            dataset_size=self._samples_per_peer,
            rounds=rounds_completed,
            delta=self.config.delta,
        )
        result = SimulationResult(
            round_idx=self._round,
            aggregator_id=aggregator.peer_id,
            accepted_updates=len(accepted),
            accuracy=accuracy,
            loss=loss,
            epsilon=epsilon,
        )
        LOGGER.info(
            "round=%s aggregator=%s accepted=%s accuracy=%.3f epsilon=%.3f",
            result.round_idx,
            result.aggregator_id,
            result.accepted_updates,
            result.accuracy,
            result.epsilon,
        )
        return result

    def simulate(self, rounds: int) -> list[SimulationResult]:
        history: list[SimulationResult] = []
        for _ in range(rounds):
            history.append(self.run_round())
        return history
