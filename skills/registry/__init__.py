"""
NEXA Africa Operating System
File: skills/registry/manifest.py
Constitutional Owner: Bill Odhiambo Othieno
Description: SkillManifest — declares a skill's identity, tier, and required
             permissions, per core/contracts/skills/skills_contract_v1.md.
             Declaring a permission does not grant it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

VALID_TIERS = ("builtin", "community", "enterprise", "privileged")


@dataclass(frozen=True)
class SkillManifest:
    """
    Immutable description of a skill.

    required_permissions is a declaration only — it is not an
    authorization grant. SkillAuthorizationGate checks it against a
    caller's actual granted permissions before any handler is released.
    """

    skill_id: str
    name: str
    description: str
    tier: str
    required_permissions: Tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not isinstance(self.skill_id, str) or not self.skill_id.strip():
            raise ValueError("SkillManifest.skill_id must be a non-empty string.")

        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("SkillManifest.name must be a non-empty string.")

        if self.tier not in VALID_TIERS:
            raise ValueError(
                f"SkillManifest.tier must be one of {VALID_TIERS}, got {self.tier!r}."
            )

        for permission in self.required_permissions:
            if not isinstance(permission, str) or not permission.strip():
                raise ValueError(
                    "Every entry in required_permissions must be a non-empty string."
                )


__all__ = [
    "SkillManifest",
    "VALID_TIERS",
]
