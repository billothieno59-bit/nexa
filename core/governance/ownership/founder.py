from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Founder:
    """
    Constitutional founder of the NEXA Africa Operating System.

    This represents architectural ownership and stewardship,
    not authentication or user identity.
    """

    legal_name: str
    title: str
    project: str
    constitutional_role: str
    founder_id: str


FOUNDER = Founder(
    legal_name="Bill Odhiambo Othieno",
    title="Founder & Constitutional Architect",
    project="NEXA Africa Operating System",
    constitutional_role="Supreme Constitutional Steward",
    founder_id="NEXA-FOUNDER-001",
)


def get_founder() -> Founder:
    """Return the immutable constitutional founder."""
    return FOUNDER


__all__ = [
    "Founder",
    "FOUNDER",
    "get_founder",
]
