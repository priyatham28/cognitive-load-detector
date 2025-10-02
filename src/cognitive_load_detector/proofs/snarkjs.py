from __future__ import annotations

import json
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..config import KeyPair
from ..dp_sgd import DPSGDOutcome, FloatArray
from .base import Proof, ProofSystem


@dataclass(frozen=True)
class SnarkJSConfig:
    """Configuration pointing to snarkjs artefacts."""

    circuit_path: Path
    proving_key_path: Path
    verification_key_path: Path

    def ensure(self) -> None:
        for item in (self.circuit_path, self.proving_key_path, self.verification_key_path):
            if not item.exists():
                raise FileNotFoundError(f"snarkjs artefact missing: {item}")


class SnarkJSProofSystem(ProofSystem):
    """Delegates proof generation/verification to `snarkjs` CLI."""

    def __init__(self, config: SnarkJSConfig, *, snarkjs_bin: str = "snarkjs") -> None:
        self._config = config
        self._snarkjs = snarkjs_bin
        self._config.ensure()

    def generate_keypair(self, seed: str | None = None) -> KeyPair:  # noqa: ARG002 - interface parity
        verifying_key = json.dumps({"vk": str(self._config.verification_key_path)})
        proving_key = json.dumps({"pk": str(self._config.proving_key_path)})
        return KeyPair(proving_key=proving_key, verifying_key=verifying_key)

    def prove(
        self,
        *,
        outcome: DPSGDOutcome,
        round_idx: int,
        keypair: KeyPair,
        clip_norm: float,
        noise_multiplier: float,
    ) -> Proof:
        with tempfile.TemporaryDirectory() as tmp:
            witness_path = Path(tmp) / "witness.json"
            public_path = Path(tmp) / "public.json"
            proof_path = Path(tmp) / "proof.json"

            payload = {
                "round": round_idx,
                "clip_norm": clip_norm,
                "noise_multiplier": noise_multiplier,
                "noisy_gradient": outcome.noisy_gradients.tolist(),
                "clipped_gradient": outcome.clipped_gradients.tolist(),
                "noise": outcome.noise.tolist(),
            }
            witness_path.write_text(json.dumps(payload))

            self._run_snarkjs(
                "groth16",
                "prove",
                str(self._config.circuit_path),
                json.loads(keypair.proving_key)["pk"],
                str(witness_path),
                str(proof_path),
                str(public_path),
            )

            commitment = proof_path.read_text()
            proof_payload = json.loads(public_path.read_text())

        return Proof(
            round=round_idx,
            clip_norm=clip_norm,
            noise_multiplier=noise_multiplier,
            payload=proof_payload,
            commitment=commitment,
        )

    def verify(
        self,
        *,
        noisy_gradient: FloatArray,
        proof: Proof,
        verifying_key: str,
    ) -> bool:
        with tempfile.TemporaryDirectory() as tmp:
            proof_path = Path(tmp) / "proof.json"
            public_path = Path(tmp) / "public.json"
            proof_path.write_text(proof.commitment)
            public_path.write_text(json.dumps(proof.payload))
            result = self._run_snarkjs(
                "groth16",
                "verify",
                json.loads(verifying_key)["vk"],
                str(public_path),
                str(proof_path),
            )
        return result.returncode == 0

    def _run_snarkjs(self, *args: Any) -> subprocess.CompletedProcess[str]:
        cmd = [self._snarkjs, *map(str, args)]
        return subprocess.run(cmd, check=False, capture_output=True, text=True)
