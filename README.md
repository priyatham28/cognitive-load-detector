# FLZK — Verifiable Browser-Based Peer-to-Peer Federated Learning

This repository mirrors the system described in the paper **“FLZK: Verifiable Browser-Based Peer-to-Peer Federated Learning with Zero-Knowledge DP-SGD.”** It provides a reproducible simulation of the protocol, developer tooling, and documentation artefacts that map directly to the sections of the research article.

## Highlights
- **Decentralised training loop.** `flzk.network.FLZKNetwork` recreates the WebRTC mesh described in Section 4, rotates aggregation duties, and emits structured telemetry for observability.
- **Pluggable proof systems.** `flzk.proofs` exposes both a deterministic development backend and a `snarkjs` integration point so practitioners can drop in real Groth16 circuits (Section 6).
- **Differential privacy with auditability.** `flzk.dp_sgd` implements clipped DP-SGD while `flzk.privacy` now uses a Rényi DP accountant mirroring the paper’s privacy analysis (Sections 5 and 9.2).
- **Browser-friendly stack.** The FastAPI service exposes simulation endpoints that a browser or Streamlit dashboard can consume to emulate the WebAssembly/WebGPU client (Section 7).

## Quickstart
```bash
make setup            # create venv and install requirements
make run              # launch FastAPI service on http://127.0.0.1:8000
make demo             # open the Streamlit dashboard
make test             # run unit tests covering DP-SGD, proofs, and the network
```

### Invoke the simulator via HTTP
```bash
curl -X POST http://127.0.0.1:8000/simulate \
  -H "content-type: application/json" \
  -d '{"rounds": 5, "num_peers": 6, "samples_per_peer": 256, "clip_norm": 1.0,
       "noise_multiplier": 1.1, "learning_rate": 0.1, "batch_size": 32, "num_features": 8,
       "proof_backend": "mock"}'
```
Returns per-round accuracy, loss, privacy budget, and the aggregator that validated each batch of zk proofs.

### Using a snarkjs backend
Provide Groth16 artefacts and set:
```bash
export FLZK_SNARKJS_CIRCUIT=path/to/circuit.wasm
export FLZK_SNARKJS_PROVING_KEY=path/to/proving_key.zkey
export FLZK_SNARKJS_VERIFICATION_KEY=path/to/verification_key.json
```
Then call the API with `"proof_backend": "snarkjs"`. The service will proxy proof generation and verification to the CLI, aligning with the paper’s production deployment.

## Reference
The original research paper is included at `docs/final_vector_camera_ready_full.pdf` for convenience.

## Repository Map
- `src/flzk/` — Core protocol components:
  - `dataset.py`: synthetic data generator matching Section 8 experimental setup.
  - `dp_sgd.py`: gradient computation, clipping, and noisy updates (Section 5).
  - `proofs/`: pluggable proof backends (`MockProofSystem`, `SnarkJSProofSystem`).
  - `peer.py`: browser peer abstraction with key management and local training.
  - `network.py`: orchestrates peer discovery, rotation, aggregation, and logging (Section 4).
  - `privacy.py`: Rényi DP accountant mirroring the paper’s analysis.
- `src/app.py` — FastAPI service exposing `/health` and `/simulate` for automation.
- `demo/streamlit_app.py` — Browser-style dashboard reflecting Section 7’s developer toolkit.
- `datasheet.md` & `model_card.md` — Documentation artefacts aligned with the paper’s Datasheet and Model Card appendices.
- `tests/` — Unit tests covering DP-SGD mechanics, proof verification, and network rollout.

## Reproducing Paper Scenarios
The simulator approximates the experiments from Section 8:
1. Choose the number of peers and samples to emulate the CIFAR (image) vs. WISDM (sensor) settings.
2. Adjust `clip_norm` and `noise_multiplier` to explore the privacy–utility trade-offs from Section 9.2.
3. Use the Streamlit dashboard or API telemetry to observe zk proof acceptance rates and privacy budget accumulation in real time.

While the mock backend provides fast iteration, the snarkjs integration demonstrates how to connect genuine Groth16 artefacts, keeping the codebase production-ready without compromising testability.

## CI/CD
GitHub Actions lint, type-check, test, and smoke the API on each push. A Dockerfile is provided to containerise the FastAPI service for deployment or larger-scale simulations.

## Citation
If you reuse this artefact, please cite the original paper and link back to this repository.
