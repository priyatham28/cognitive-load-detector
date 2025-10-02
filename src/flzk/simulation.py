"""Core simulation utilities for the FLZK demo service.

The real FLZK system combines differential privacy with verifiable computation.
For this repository we provide a lightweight, deterministic simulator that
mimics the behaviour of a federated learning round while remaining easy to test
and reason about. The module is intentionally small but structured so teams can
swap in production logic later.
"""

from __future__ import annotations

import math
import statistics
from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class SimulationConfig:
    """Configuration for the simulation run."""

    rounds: int = 5
    num_peers: int = 4
    samples_per_peer: int = 256
    clip_norm: float = 1.0
    noise_multiplier: float = 1.1
    learning_rate: float = 0.1
    batch_size: int = 32
    num_features: int = 8


@dataclass(frozen=True)
class SimulationMetric:
    """Metrics emitted for a single round."""

    round: int
    accuracy: float
    loss: float


@dataclass(frozen=True)
class SimulationSummary:
    """Aggregated results of a simulation run."""

    metrics: List[SimulationMetric]
    epsilon: float
    delta: float
    backend: str

    @property
    def final_accuracy(self) -> float:
        """Return the accuracy from the last recorded round."""

        return self.metrics[-1].accuracy

    @property
    def average_loss(self) -> float:
        """Return the average loss across the run."""

        return statistics.fmean(metric.loss for metric in self.metrics)


def _compute_epsilon(config: SimulationConfig) -> float:
    """Compute a toy privacy budget using a simplified accountant.

    This is intentionally approximate; the focus is on producing deterministic
    output that feels plausible to demo consumers.
    """

    sampling_probability = config.batch_size / max(config.samples_per_peer * config.num_peers, 1)
    base = sampling_probability / max(config.noise_multiplier, 1e-6)
    return round(math.log1p(base) * config.rounds * 3.5, 4)


def run_simulation(config: SimulationConfig, *, backend: str = "mock") -> SimulationSummary:
    """Run a deterministic simulation producing synthetic metrics.

    Args:
        config: Parameters that influence convergence trends.
        backend: Name of the proof backend selected by the caller (e.g. "mock").

    Returns:
        SimulationSummary with per-round accuracy/loss and privacy metadata.
    """

    metrics = []
    accuracy = 0.78
    loss = 0.62

    for current_round in range(1, config.rounds + 1):
        # TODO(ml-team): Swap to real federated training metrics once the DP stack lands.
        accuracy = round(min(0.99, accuracy + 0.004 + config.learning_rate * 0.02), 4)
        loss = round(max(0.05, loss - 0.006 - config.learning_rate * 0.01), 4)
        metrics.append(SimulationMetric(round=current_round, accuracy=accuracy, loss=loss))

    epsilon = _compute_epsilon(config)
    summary = SimulationSummary(metrics=metrics, epsilon=epsilon, delta=1e-5, backend=backend)
    return summary


def summarise_metrics(metrics: Iterable[SimulationMetric]) -> dict[str, float]:
    """Return convenience aggregations for notebooks and dashboards."""

    metrics_list = list(metrics)
    return {
        "max_accuracy": max((m.accuracy for m in metrics_list), default=0.0),
        "min_loss": min((m.loss for m in metrics_list), default=0.0),
        "rounds": len(metrics_list),
    }
