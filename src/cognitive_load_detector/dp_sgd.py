from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from .config import TrainingConfig


FloatArray = NDArray[np.float64]
IntArray = NDArray[np.int64]


def _sigmoid(logits: FloatArray) -> FloatArray:
    return 1.0 / (1.0 + np.exp(-logits))


@dataclass
class DPSGDOutcome:
    gradients: FloatArray
    clipped_gradients: FloatArray
    noisy_gradients: FloatArray
    noise: FloatArray
    grad_norm: float


def logistic_gradient(
    weights: FloatArray,
    batch_x: FloatArray,
    batch_y: IntArray,
) -> FloatArray:
    """Compute the gradient of the logistic loss for a batch."""

    logits = batch_x @ weights
    probs = _sigmoid(logits)
    error = probs - batch_y
    grad = (batch_x.T @ error) / batch_x.shape[0]
    return grad.astype(np.float64)


def dp_sgd_step(
    *,
    weights: FloatArray,
    batch_x: FloatArray,
    batch_y: IntArray,
    config: TrainingConfig,
    rng: np.random.Generator,
) -> DPSGDOutcome:
    """Run one DP-SGD step returning gradients and noisy update."""

    grad = logistic_gradient(weights, batch_x, batch_y)
    grad_norm = float(np.linalg.norm(grad) + 1e-12)
    clip_scale = min(1.0, config.clip_norm / grad_norm)
    clipped = grad * clip_scale
    noise_std = config.noise_multiplier * config.clip_norm
    noise = rng.normal(loc=0.0, scale=noise_std, size=grad.shape)
    noisy_grad = clipped + noise
    return DPSGDOutcome(
        gradients=grad,
        clipped_gradients=clipped,
        noisy_gradients=noisy_grad,
        noise=noise,
        grad_norm=grad_norm,
    )


def apply_update(
    weights: FloatArray,
    noisy_gradient: FloatArray,
    *,
    learning_rate: float,
) -> FloatArray:
    """Perform the model update using the noisy gradient."""

    return weights - learning_rate * noisy_gradient


def logistic_accuracy(
    weights: FloatArray,
    features: FloatArray,
    labels: IntArray,
) -> float:
    """Compute accuracy to evaluate global model quality."""

    logits = features @ weights
    preds = (logits >= 0.0).astype(np.int64)
    return float(np.mean(preds == labels))


def logistic_loss(
    weights: FloatArray,
    features: FloatArray,
    labels: IntArray,
) -> float:
    """Average logistic loss using numerically stable computation."""

    logits = features @ weights
    loss = np.logaddexp(0.0, -logits * (2 * labels - 1)).mean()
    return float(loss)
