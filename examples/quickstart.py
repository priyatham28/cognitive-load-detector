"""Quickstart example for the Cognitive Load Detector simulator."""

from __future__ import annotations

from cognitive_load_detector import (
    CognLoadNetwork,
    MockProofSystem,
    TrainingConfig,
)


def main() -> None:
    config = TrainingConfig(
        clip_norm=1.0,
        noise_multiplier=1.0,
        learning_rate=0.1,
        batch_size=16,
    )
    network = CognLoadNetwork(
        num_peers=4,
        samples_per_peer=128,
        num_features=6,
        config=config,
        seed=1234,
        proof_system=MockProofSystem(),
    )
    history = network.simulate(rounds=3)
    final = history[-1]
    print("Rounds simulated:", len(history))
    print("Final accuracy:", f"{final.accuracy:.3f}")
    print("Final epsilon:", f"{final.epsilon:.3f}")


if __name__ == "__main__":
    main()
