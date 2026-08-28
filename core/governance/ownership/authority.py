from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from core.governance.ownership.founder import FOUNDER


class AuthorityLevel(str, Enum):
    FOUNDER = "founder"
    CONSTITUTION = "constitution"
    MODULE = "module"
    PUBLIC = "public"


@dataclass(frozen=True)
class ConstitutionalAuthority:
    owner: str
    project: str
    level: AuthorityLevel
    immutable: bool


NEXA_AUTHORITY = ConstitutionalAuthority(
    owner=FOUNDER.legal_name,
    project=FOUNDER.project,
    level=AuthorityLevel.FOUNDER,
    immutable=True,
)


def get_authority() -> ConstitutionalAuthority:
    return NEXA_AUTHORITY


__all__ = [
    "AuthorityLevel",
    "ConstitutionalAuthority",
    "NEXA_AUTHORITY",
    "get_authority",
]
