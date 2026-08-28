"""
NEXA Africa Operating System
File: skills/privileged/system_shutdown.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Privileged skill wrapping ShutdownController. Requires the
             SYSTEM.SHUTDOWN skill permission (derived from a real
             TrustSession via skills/registry/trust_bridge.py) to even
             be handed out by SkillAuthorizationGate, AND still requires
             the correct NEXA_EMERGENCY_KEY at the ShutdownController
             layer itself. Two independent checks, not a shortcut
             around either one.
"""

from __future__ import annotations

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry
from core.governance.trust.shutdown.controller import ShutdownController

SYSTEM_SHUTDOWN_SKILL = SkillManifest(
    skill_id="system.shutdown_nexa",
    name="Shutdown NEXA",
    description="Requests an emergency shutdown of the NEXA process.",
    tier="privileged",
    required_permissions=("SYSTEM.SHUTDOWN",),
)

_controller = ShutdownController()


def _shutdown_handler(emergency_key: str):
    """
    Requires SkillAuthorizationGate permission (SYSTEM.SHUTDOWN) to be
    obtained at all, then still requires the correct emergency key to
    actually authorize via ShutdownController. Returns the
    ShutdownAuthorization result either way; never raises for a wrong key.
    """
    return _controller.request_shutdown(emergency_key)


def register_privileged_skills(registry: SkillRegistry) -> None:
    registry.register(SYSTEM_SHUTDOWN_SKILL, _shutdown_handler)


__all__ = [
    "SYSTEM_SHUTDOWN_SKILL",
    "register_privileged_skills",
]
