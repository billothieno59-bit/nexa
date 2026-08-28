"""
NEXA Africa Operating System
File: core/interaction/accessibility/profile.py
Constitutional Owner: Bill Odhiambo Othieno
Description: AccessibilityProfile — a structured, honest representation of
             a person's stated accessibility needs, per
             core/contracts/accessibility/ual_contract_v1.md. Built only
             from explicitly stated preferences, never inferred.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class AccessibilityProfile:
    """
    A person's stated accessibility preferences.

    Every field defaults to "no accommodation requested." Nothing here
    is inferred — a profile only reflects what was explicitly set.
    """

    profile_id: str
    needs_simplified_language: bool = False
    needs_screen_reader_friendly_output: bool = False
    preferred_reading_level: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.profile_id, str) or not self.profile_id.strip():
            raise ValueError("AccessibilityProfile.profile_id must be a non-empty string.")

        valid_levels = {None, "simple", "standard"}
        if self.preferred_reading_level not in valid_levels:
            raise ValueError(
                f"preferred_reading_level must be one of {valid_levels}, "
                f"got {self.preferred_reading_level!r}."
            )


__all__ = [
    "AccessibilityProfile",
]
