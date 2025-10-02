from __future__ import annotations

import numpy as np

from cognitive_load_detector.config import TrainingConfig
from cognitive_load_detector.dp_sgd import dp_sgd_step


def test_clip_norm_enforced() -> None:
    config = TrainingConfig(clip_norm=0.5, noise_multiplier=0.0, learning_rate=0.1, batch_size=4)
    rng = np.random.default_rng(42)
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

    assert np.linalg.norm(outcome.clipped_gradients) <= config.clip_norm + 1e-6


def test_noise_added_matches_scale() -> None:
    config = TrainingConfig(clip_norm=1.0, noise_multiplier=1.5, learning_rate=0.1, batch_size=4)
    rng = np.random.default_rng(0)
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

    assert outcome.noisy_gradients.shape == weights.shape
    estimated_std = float(np.std(outcome.noise))
    expected_std = config.noise_multiplier * config.clip_norm
    assert expected_std == 0 or abs(estimated_std - expected_std) < 3 * expected_std
