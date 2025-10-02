from __future__ import annotations

from cognitive_load_detector.config import TrainingConfig
from cognitive_load_detector.network import CognitiveLoadNetwork
from cognitive_load_detector.proofs import MockProofSystem


def test_network_simulation_runs() -> None:
    config = TrainingConfig(clip_norm=1.0, noise_multiplier=1.0, learning_rate=0.1, batch_size=16)
    network = CognitiveLoadNetwork(
        num_peers=4,
        samples_per_peer=64,
        num_features=4,
        config=config,
        seed=123,
        proof_system=MockProofSystem(),
    )
    history = network.simulate(3)
    assert len(history) == 3
    assert history[-1].accuracy >= 0.0
    assert history[-1].epsilon > 0.0
