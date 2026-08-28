"""
NEXA Africa Operating System
File: core/perception/events.py
Constitutional Owner: Bill Odhiambo Othieno
Description: The canonical PerceptionEvent — the single structured output
             every perception capturer must produce, per
             core/contracts/perception/upl_contract_v1.md.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True)
class PerceptionEvent:
    """
    Immutable, structured representation of a single unit of sensory
    input, as defined by the UPL contract.

    PerceptionEvent carries no linguistic or semantic interpretation.
    It only describes what was captured, from where, and when.
    """

    modality: str
    source: str
    payload: Any
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.modality, str) or not self.modality.strip():
            raise ValueError("PerceptionEvent.modality must be a non-empty string.")

        if not isinstance(self.source, str) or not self.source.strip():
            raise ValueError("PerceptionEvent.source must be a non-empty string.")


__all__ = [
    "PerceptionEvent",
]
