"""Core package for the FLZK peer-to-peer DP-SGD simulation."""

from .config import Dataset, KeyPair, TrainingConfig
from .dataset import generate_synthetic_dataset
from .dp_sgd import DPSGDOutcome, FloatArray, dp_sgd_step
from .network import FLZKNetwork, SimulationResult
from .peer import FLZKPeer, LocalUpdate
from .privacy import approximate_epsilon
from .proofs import (
    MockProofSystem,
    Proof,
    ProofSystem,
    SnarkJSConfig,
    SnarkJSProofSystem,
)

__all__ = [
    "Dataset",
    "KeyPair",
    "TrainingConfig",
    "generate_synthetic_dataset",
    "dp_sgd_step",
    "DPSGDOutcome",
    "FloatArray",
    "FLZKPeer",
    "LocalUpdate",
    "FLZKNetwork",
    "SimulationResult",
    "approximate_epsilon",
    "Proof",
    "ProofSystem",
    "MockProofSystem",
    "SnarkJSConfig",
    "SnarkJSProofSystem",
]
