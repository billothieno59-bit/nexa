from __future__ import annotations

from dataclasses import dataclass

from core.governance.ownership.founder import FOUNDER


@dataclass(frozen=True)
class IntellectualProperty:
    project: str
    owner: str
    copyright_notice: str
    canonical_name: str


IP = IntellectualProperty(
    project="NEXA Africa Operating System",
    owner=FOUNDER.legal_name,
    copyright_notice=(
        "Copyright (c) Bill Odhiambo Othieno. "
        "All Constitutional Architecture Rights Reserved."
    ),
    canonical_name="NEXA Africa Operating System",
)


def get_ip() -> IntellectualProperty:
    return IP


__all__ = [
    "IntellectualProperty",
    "IP",
    "get_ip",
]
