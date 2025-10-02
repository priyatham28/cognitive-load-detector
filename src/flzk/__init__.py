"""FLZK simulation package.

This package exposes a deterministic simulation that mirrors the shape of the
original FLZK protocol without depending on heavyweight cryptography stacks.
It is designed as a starting point for teams experimenting with verifiable
federated learning in Python.
"""

from __future__ import annotations

from .simulation import SimulationConfig, SimulationMetric, SimulationSummary, run_simulation, summarise_metrics

DESCRIPTION = "Verifiable browser-based P2P federated learning demo"

__all__ = [
    "SimulationConfig",
    "SimulationMetric",
    "SimulationSummary",
    "run_simulation",
    "summarise_metrics",
    "DESCRIPTION",
]
