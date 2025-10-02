from __future__ import annotations

import secrets
from dataclasses import dataclass
from hashlib import blake2s

import numpy as np

from ..config import KeyPair
from ..dp_sgd import DPSGDOutcome, FloatArray
from .base import Proof, ProofSystem


@dataclass(frozen=True)
class _MaskPayload:
    masked_clipped: list[float]
    masked_noise: list[float]

    def export(self) -> dict[str, list[float]]:
        return {
            "masked_clipped": self.masked_clipped,
            "masked_noise": self.masked_noise,
        }


class MockProofSystem(ProofSystem):
    """Deterministic masking scheme used for local development and tests."""

    def generate_keypair(self, seed: str | None = None) -> KeyPair:
        if seed is None:
            seed = secrets.token_hex(16)
        proving_key = blake2s(f"prove:{seed}".encode(), digest_size=32).hexdigest()
        verifying_key = blake2s(f"verify:{proving_key}".encode(), digest_size=32).hexdigest()
        return KeyPair(proving_key=proving_key, verifying_key=verifying_key)

    def _derive_mask(self, verifying_key: str, round_idx: int, size: int) -> FloatArray:
        seed_material = f"{verifying_key}:{round_idx}".encode()
        digest = blake2s(seed_material, digest_size=32).digest()
        seed = int.from_bytes(digest, byteorder="big", signed=False)
        rng = np.random.default_rng(seed)
        return rng.normal(0.0, 1.0, size=size)

    def prove(
        self,
        *,
        outcome: DPSGDOutcome,
        round_idx: int,
        keypair: KeyPair,
        clip_norm: float,
        noise_multiplier: float,
    ) -> Proof:
        mask = self._derive_mask(keypair.verifying_key, round_idx, outcome.noisy_gradients.size)
        masked_clipped = (outcome.clipped_gradients + mask).astype(float)
        masked_noise = (outcome.noise + mask).astype(float)
        payload = _MaskPayload(masked_clipped.tolist(), masked_noise.tolist())
        commitment = self._commit(masked_clipped, masked_noise, keypair.verifying_key)
        return Proof(
            round=round_idx,
            clip_norm=clip_norm,
            noise_multiplier=noise_multiplier,
            payload=payload.export(),
            commitment=commitment,
        )

    def _commit(self, masked_clipped: FloatArray, masked_noise: FloatArray, verifying_key: str) -> str:
        payload = np.concatenate([masked_clipped, masked_noise]).astype(np.float64).tobytes()
        return blake2s(payload + verifying_key.encode(), digest_size=32).hexdigest()

    def verify(
        self,
        *,
        noisy_gradient: FloatArray,
        proof: Proof,
        verifying_key: str,
        atol: float = 1e-5,
    ) -> bool:
        mask = self._derive_mask(verifying_key, proof.round, noisy_gradient.size)
        masked_clipped = np.asarray(proof.payload["masked_clipped"], dtype=float)
        masked_noise = np.asarray(proof.payload["masked_noise"], dtype=float)
        expected_commit = self._commit(masked_clipped, masked_noise, verifying_key)
        if expected_commit != proof.commitment:
            return False

        clipped = masked_clipped - mask
        noise = masked_noise - mask

        if np.linalg.norm(clipped) - proof.clip_norm > 1e-4:
            return False

        if not np.allclose(clipped + noise, noisy_gradient, atol=atol):
            return False

        expected_std = proof.noise_multiplier * proof.clip_norm
        if noise.size >= 8 and expected_std > 0:
            estimated_std = float(np.std(noise))
            if abs(estimated_std - expected_std) / max(expected_std, 1e-12) > 0.5:
                return False
        return True
