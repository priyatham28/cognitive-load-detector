# Datasheet for Cognitive Load Detector Simulation Assets

This datasheet follows the structure proposed in Appendix A of the FLZK paper.

## Motivation
- **Purpose.** Provide a reproducible, privacy-aware federated dataset for evaluating the FLZK
  pipeline end-to-end without distributing sensitive raw data.
- **Tasks.** Binary classification matching the image (CIFAR-10 subset) and mobile sensor (WISDM)
  experiments in the paper.

## Composition
- Synthetic mixtures of Gaussians with configurable dimensionality (`num_features`).
- Each peer receives an independent sample of size `samples_per_peer`, reflecting the non-IID
  distributions described in Section 8.1.
- Labels are balanced but can exhibit class skew depending on the random seed, reproducing
  heterogeneity across peers.

## Collection & Pre-processing
- Generated on demand using `cognitive_load_detector.dataset.generate_synthetic_dataset` with an
  RNG seed; no real-world collection occurs.
- Features are standardised and augmented with a bias term to match the logistic regression
  backbone used for evaluation.
- No personal or sensitive attributes are ever present.

## Uses
- Validate DP-SGD implementation and zero-knowledge verification logic with either the mock or
  snarkjs proof backend.
- Benchmark communication/aggregation strategies by varying peers, batch sizes, and noise
  multipliers.
- Stress-test the Rényi DP accountant by sweeping hyper-parameters across realistic regimes.

## Distribution
- Created locally at runtime; nothing is redistributed.
- Licensed under the repository’s MIT licence (synthetic data only).

## Maintenance
- Parameter defaults align with the paper; updates will follow revisions of the research artefact.
- Issues or improvements can be filed via GitHub.
