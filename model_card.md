# Model Card: FLZK Logistic Backbone

This card summarises the model simulated inside the FLZK protocol.

## Overview
- **Architecture.** Logistic regression classifier trained collaboratively across browser peers.
- **Objective.** Mirror the verification and privacy characteristics of the FLZK framework while allowing drop-in Groth16 proof systems during experimentation.

## Intended Use
- Research prototyping, pedagogy, and regression testing of the FLZK pipeline.
- Demonstrating proof backends by switching between the mock masking scheme and a `snarkjs`-powered Groth16 circuit.

## Training Data
- Synthetic Gaussian mixtures generated per peer (see `datasheet.md`).
- Each peer sees a unique distribution, modelling non-IID conditions described in Section 8 of the paper.

## Metrics
- Accuracy and logistic loss logged after every round.
- Privacy tracked via an analytical Rényi DP accountant.
- Proof acceptance monitored through per-round telemetry to surface verification failures.

## Ethical Considerations & Limitations
- Synthetic data avoids privacy risk but does not capture complex real-world correlations.
- Groth16 integration depends on the correctness of user-provided circuits; this repository does not ship audited circuits.
- The DP accountant uses integer Rényi orders up to 64; extreme hyper-parameters may require tighter analysis.

## Maintenance & Versioning
- `SimulationResult` objects carry metadata for auditing.
- Changes to DP parameters, proof integrations, or circuit interfaces should increment semantic versions and update this card accordingly.
