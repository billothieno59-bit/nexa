"""
NEXA Africa Operating System
File: core/interaction/accessibility/registry.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Stores and retrieves AccessibilityProfiles by profile_id, per
             core/contracts/accessibility/ual_contract_v1.md.
"""

from __future__ import annotations

from typing import Dict, Optional

from core.interaction.accessibility.profile import AccessibilityProfile
from core.services.logging.logger import get_logger

logger = get_logger(__name__)


class AccessibilityProfileRegistry:
    """
    In-memory registry of accessibility profiles by profile_id.
    """

    def __init__(self) -> None:
        self._profiles: Dict[str, AccessibilityProfile] = {}

    def register(self, profile: AccessibilityProfile) -> None:
        if not isinstance(profile, AccessibilityProfile):
            raise TypeError(
                "AccessibilityProfileRegistry.register() requires an AccessibilityProfile."
            )

        self._profiles[profile.profile_id] = profile
        logger.info("Registered accessibility profile id=%s", profile.profile_id)

    def get(self, profile_id: str) -> Optional[AccessibilityProfile]:
        return self._profiles.get(profile_id)

    def remove(self, profile_id: str) -> bool:
        if profile_id in self._profiles:
            del self._profiles[profile_id]
            logger.info("Removed accessibility profile id=%s", profile_id)
            return True
        return False


global_accessibility_registry = AccessibilityProfileRegistry()


__all__ = [
    "AccessibilityProfileRegistry",
    "global_accessibility_registry",
]
