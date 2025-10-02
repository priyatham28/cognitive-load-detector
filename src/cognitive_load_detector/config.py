from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np
from numpy.typing import NDArray


FloatArray = NDArray[np.float64]
IntArray = NDArray[np.int64]


@dataclass(frozen=True)
class TrainingConfig:
    """Hyperparameters controlling DP-SGD behaviour."""

    clip_norm: float
    noise_multiplier: float
    learning_rate: float
    batch_size: int
    delta: float = 1e-5


@dataclass(frozen=True)
class KeyPair:
    """Simple stand-in for a zk-SNARK proving and verification key pair."""

    proving_key: str
    verifying_key: str


Dataset = Tuple[FloatArray, IntArray]
