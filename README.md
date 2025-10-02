# Cognitive Load Detector — FLZK-Inspired Federated Simulation

![CI](https://github.com/priyatham28/cognitive-load-detector/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

This project packages a recruit-ready implementation of the **FLZK** protocol—browser-friendly
federated learning with differential privacy and zero-knowledge verification—under a
`cognitive-load-detector` Python package. It ships with a FastAPI service, Streamlit dashboard,
unit-tested core logic, and packaging/CI tooling so reviewers can install and run the system with
minimal friction.

## Features
- **Decentralised training loop** – `cognitive_load_detector.network.CognitiveLoadNetwork`
  simulates peer rotation, FedAvg aggregation, and telemetry.
- **Pluggable proof systems** – toggle between a deterministic mock backend or a Groth16
  `snarkjs` integration for real zero-knowledge proofs.
- **Differential privacy analytics** – a Rényi DP accountant tracks the privacy budget across
  rounds.
- **Production-ready tooling** – `make`, Docker, CI, packaging (`pip install .`), datasheet and
  model card are all included.

## Installation
```bash
# optional: create a fresh virtual environment
python -m venv .venv && . .venv/bin/activate

# install the project + dev tooling
git clone https://github.com/priyatham28/cognitive-load-detector.git
cd cognitive-load-detector
pip install -U pip
pip install -r requirements.txt
```

### Quickstart
```bash
make run &                     # start the FastAPI service on :8000
curl -f http://127.0.0.1:8000/health
curl -s -X POST http://127.0.0.1:8000/simulate \
  -H "content-type: application/json" \
  -d '{"rounds": 2, "num_peers": 4, "samples_per_peer": 128,
       "clip_norm": 1.0, "noise_multiplier": 1.0,
       "learning_rate": 0.1, "batch_size": 32,
       "num_features": 6, "proof_backend": "mock"}' | jq
```
Example output snippet:
```json
{
  "history": [
    {"round_idx": 1, "aggregator_id": "peer-2", "accuracy": 0.55, ...},
    {"round_idx": 2, "aggregator_id": "peer-1", "accuracy": 0.63, ...}
  ],
  "final_accuracy": 0.63,
  "final_loss": 0.64,
  "final_epsilon": 0.92
}
```

### Developer Workflow
```bash
make setup      # create venv + install deps
make test       # pytest
make lint       # ruff linting
make type       # mypy static checks
make demo       # Streamlit dashboard
make build      # python -m build (sdist + wheel)
```

### snarkjs Backend
Provide Groth16 artefacts and export:
```bash
export CLD_SNARKJS_CIRCUIT=path/to/circuit.wasm
export CLD_SNARKJS_PROVING_KEY=path/to/proving_key.zkey
export CLD_SNARKJS_VERIFICATION_KEY=path/to/verification_key.json
```
Then call `/simulate` with `{"proof_backend": "snarkjs"}`. The service proxies proof generation
and verification to `snarkjs`.

## Project Layout
- `src/cognitive_load_detector/` – core package (config, dataset, DP-SGD, proofs, network, API).
- `examples/quickstart.py` – run a mini-training loop from a script.
- `demo/streamlit_app.py` – GUI for experimenting with parameters.
- `tests/` – unit tests covering DP-SGD, proof generation, and network orchestration.
- `Dockerfile` – container image exposing FastAPI on port 8000.
- `model_card.md`, `datasheet.md` – documentation referencing the research lineage.
- `docs/final_vector_camera_ready_full.pdf` – reference paper.

## Contributing
1. Fork the repository & create a feature branch.
2. Install dev dependencies via `pip install -r requirements.txt`.
3. Run `make lint test type` before pushing.
4. Open a pull request describing your change and test coverage.

Please see the [Model Card](model_card.md) and [Datasheet](datasheet.md) for ethical
and data considerations.

## License
Released under the [MIT License](LICENSE).
