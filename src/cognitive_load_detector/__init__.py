"""Core package for the Cognitive Load Detector federated simulation."""

from .config import Dataset, KeyPair, TrainingConfig
from .dataset import generate_synthetic_dataset
from .dp_sgd import DPSGDOutcome, FloatArray, dp_sgd_step
from .network import CognitiveLoadNetwork, SimulationResult
from .peer import CognitiveLoadPeer, LocalUpdate
from .privacy import approximate_epsilon
from .proofs import (
    MockProofSystem,
    Proof,
    ProofSystem,
    SnarkJSConfig,
    SnarkJSProofSystem,
)

# Backwards-compatible alias for earlier module name.
CognLoadNetwork = CognitiveLoadNetwork

__all__ = [
    "Dataset",
    "KeyPair",
    "TrainingConfig",
    "generate_synthetic_dataset",
    "dp_sgd_step",
    "DPSGDOutcome",
    "FloatArray",
    "CognitiveLoadPeer",
    "LocalUpdate",
    "CognitiveLoadNetwork",
    "CognLoadNetwork",
    "SimulationResult",
    "approximate_epsilon",
    "Proof",
    "ProofSystem",
    "MockProofSystem",
    "SnarkJSConfig",
    "SnarkJSProofSystem",
]
