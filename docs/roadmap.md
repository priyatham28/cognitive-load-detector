# Roadmap

## v0.2.0 (In progress)
- Integrate stochastic noise into the simulator and expose seed control.
- Serve OpenAPI schema and add typed client bindings (httpx-based).
- Publish packages to TestPyPI via release workflow.

## v0.3.0
- Experiment with real DP-SGD via Opacus or TensorFlow Privacy.
- Swap the mock proof backend with a stub calling `snarkjs` or HyperPlonk.
- Add distributed tracing hooks (OTel) to the FastAPI stack.

## Nice-to-haves
- Add GitHub Discussions and project board for community triage.
- Expand dataset catalogue beyond synthetic Gaussian blends.
- Mirror repository docs to a hosted site using `mkdocs-material`.

> TODO(product): Align roadmap with research milestones once zk proof PoC is complete.
