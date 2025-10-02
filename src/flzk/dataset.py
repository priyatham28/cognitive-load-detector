from __future__ import annotations

import numpy as np

from .config import Dataset, FloatArray, IntArray


def generate_synthetic_dataset(
    *,
    num_samples: int,
    num_features: int,
    rng: np.random.Generator,
    class_sep: float = 2.0,
) -> Dataset:
    """Create a lightweight binary classification dataset."""

    origins: FloatArray = rng.normal(loc=0.0, scale=class_sep, size=(2, num_features))
    labels: IntArray = rng.integers(low=0, high=2, size=num_samples, endpoint=False).astype(np.int64)
    features = origins[labels] + rng.normal(scale=1.0, size=(num_samples, num_features))
    bias = np.ones((num_samples, 1), dtype=features.dtype)
    return np.hstack([features, bias]).astype(np.float64), labels
