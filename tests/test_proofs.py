from __future__ import annotations

import numpy as np

from flzk.config import TrainingConfig
from flzk.dp_sgd import dp_sgd_step
from flzk.proofs import MockProofSystem


def test_proof_roundtrip() -> None:
    config = TrainingConfig(clip_norm=1.0, noise_multiplier=1.0, learning_rate=0.1, batch_size=4)
    rng = np.random.default_rng(1)
    weights = np.zeros(3)
    features = rng.normal(size=(4, 3))
    labels = rng.integers(0, 2, size=4).astype(np.int64)

    outcome = dp_sgd_step(
        weights=weights,
        batch_x=features,
        batch_y=labels,
        config=config,
        rng=rng,
    )
    proof_system = MockProofSystem()
    keypair = proof_system.generate_keypair("unit-test")
    proof = proof_system.prove(
        outcome=outcome,
        round_idx=0,
        keypair=keypair,
        clip_norm=config.clip_norm,
        noise_multiplier=config.noise_multiplier,
    )

    assert proof_system.verify(
        noisy_gradient=outcome.noisy_gradients,
        proof=proof,
        verifying_key=keypair.verifying_key,
    )
