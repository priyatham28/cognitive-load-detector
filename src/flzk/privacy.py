from __future__ import annotations

import math
from typing import Iterable


def _log_sum_exp(values: Iterable[float]) -> float:
    values = list(values)
    max_val = max(values)
    if math.isinf(max_val):
        return max_val
    total = sum(math.exp(v - max_val) for v in values)
    return max_val + math.log(total)


def _rdp_sampled_gaussian(q: float, noise_multiplier: float, order: int) -> float:
    if q == 0:
        return 0.0
    if noise_multiplier == 0:
        return math.inf
    if order <= 1:
        raise ValueError("RDP order must be > 1")

    log_a_values = []
    sigma_sq = noise_multiplier ** 2
    for i in range(order + 1):
        if i == 0:
            log_comb = 0.0
        else:
            log_comb = math.log(math.comb(order, i))
        log_prob = i * math.log(q) + (order - i) * math.log1p(-q)
        exponent = (i * (i - 1)) / (2 * sigma_sq)
        log_a_values.append(log_comb + log_prob + exponent)
    log_sum = _log_sum_exp(log_a_values)
    return log_sum / (order - 1)


def approximate_epsilon(
    *,
    noise_multiplier: float,
    batch_size: int,
    dataset_size: int,
    rounds: int,
    delta: float,
) -> float:
    """Analytical moments accountant for DP-SGD using Rényi DP."""

    if batch_size <= 0 or dataset_size <= 0 or rounds <= 0:
        return 0.0
    if noise_multiplier <= 0:
        return float("inf")
    if not (0 < delta < 1):
        raise ValueError("delta must be in (0, 1)")

    q = min(batch_size / dataset_size, 1.0)
    orders = list(range(2, 65))
    rdp_values = [rounds * _rdp_sampled_gaussian(q, noise_multiplier, order) for order in orders]

    eps_candidates = [rdp + math.log(1 / delta) / (order - 1) for rdp, order in zip(rdp_values, orders)]
    epsilon = float(min(eps_candidates))
    return epsilon
