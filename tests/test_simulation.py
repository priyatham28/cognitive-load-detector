from __future__ import annotations

from flzk import SimulationConfig, run_simulation, summarise_metrics


def test_run_simulation_trends() -> None:
    config = SimulationConfig(rounds=3, learning_rate=0.2)
    result = run_simulation(config, backend="mock")

    assert len(result.metrics) == 3
    assert result.metrics[0].accuracy < result.metrics[-1].accuracy
    assert result.metrics[0].loss > result.metrics[-1].loss
    assert result.backend == "mock"
    assert result.final_accuracy == result.metrics[-1].accuracy
    assert result.average_loss > 0

    summary = summarise_metrics(result.metrics)
    assert summary["rounds"] == 3
    assert summary["max_accuracy"] >= result.metrics[-1].accuracy
    assert summary["min_loss"] <= result.metrics[-1].loss
