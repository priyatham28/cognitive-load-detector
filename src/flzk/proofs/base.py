from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Mapping, Protocol

from ..config import KeyPair
from ..dp_sgd import DPSGDOutcome, FloatArray


@dataclass(frozen=True)
class Proof:
    """Proof artifact exchanged between FLZK peers."""

    round: int
    clip_norm: float
    noise_multiplier: float
    payload: Mapping[str, list[float] | float | str]
    commitment: str


class ProofSystem(ABC):
    """Interface for generating and verifying FLZK proofs."""

    @abstractmethod
    def generate_keypair(self, seed: str | None = None) -> KeyPair:
        """Create a proving/verification key pair bound to this backend."""

    @abstractmethod
    def prove(
        self,
        *,
        outcome: DPSGDOutcome,
        round_idx: int,
        keypair: KeyPair,
        clip_norm: float,
        noise_multiplier: float,
    ) -> Proof:
        """Produce a proof for the supplied DP-SGD outcome."""

    @abstractmethod
    def verify(
        self,
        *,
        noisy_gradient: FloatArray,
        proof: Proof,
        verifying_key: str,
    ) -> bool:
        """Check whether a peer has adhered to DP-SGD constraints."""


class SupportsExport(Protocol):
    def export(self) -> Mapping[str, list[float] | float | str]:
        ...
