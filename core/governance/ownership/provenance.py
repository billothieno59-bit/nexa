from __future__ import annotations

from dataclasses import dataclass

from core.governance.ownership.founder import FOUNDER


@dataclass(frozen=True)
class Provenance:
    project: str
    owner: str
    constitution: str
    architecture_version: str
    canonical: bool


PROVENANCE = Provenance(
    project="NEXA Africa Operating System",
    owner=FOUNDER.legal_name,
    constitution="CONSTITUTION.md",
    architecture_version="ARCHITECTURE_VERSION",
    canonical=True,
)


def get_provenance() -> Provenance:
    return PROVENANCE


__all__ = [
    "Provenance",
    "PROVENANCE",
    "get_provenance",
]
