"""
NEXA Africa Operating System
File: core/knowledge/facts.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Fact — a single piece of durable knowledge, per
             core/contracts/knowledge/ukl_contract_v1.md. Distinct from
             session memory: a Fact is meant to remain true independent
             of any one conversation.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Fact:
    """
    A single durable knowledge assertion.
    """

    subject: str
    predicate: str
    value: str
    provenance: str
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self) -> None:
        for field_name in ("subject", "predicate", "value", "provenance"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Fact.{field_name} must be a non-empty string.")


__all__ = [
    "Fact",
]
