from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from core.governance.ownership.founder import FOUNDER


@dataclass(frozen=True)
class StewardshipRecord:
    steward: str
    architecture: str
    established: str
    principle: str


STEWARDSHIP = StewardshipRecord(
    steward=FOUNDER.legal_name,
    architecture="NEXA Constitutional Architecture",
    established=datetime.now(UTC).date().isoformat(),
    principle="Architecture evolves only through constitutional versions.",
)


def get_stewardship() -> StewardshipRecord:
    return STEWARDSHIP


__all__ = [
    "StewardshipRecord",
    "STEWARDSHIP",
    "get_stewardship",
]
