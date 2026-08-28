"""
NEXA Africa Operating System
File: skills/registry/authorization.py
Constitutional Owner: Bill Odhiambo Othieno
Description: SkillAuthorizationGate — the only sanctioned way to obtain a
             skill's handler for actual invocation, per
             core/contracts/skills/skills_contract_v1.md. Fails closed:
             an unknown skill, a missing permission, or no granted
             permissions all result in denial, never a default allow.
"""

from __future__ import annotations

from typing import Callable, FrozenSet

from skills.registry.registry import SkillRegistry
from core.services.logging.logger import get_logger

logger = get_logger(__name__)


class SkillAuthorizationError(Exception):
    """Raised when a skill's handler is requested without the required permissions."""


class SkillAuthorizationGate:
    """
    Gatekeeper between a skill's declared required_permissions and
    actually obtaining its handler.

    This does not decide what permissions a caller has — it only checks
    a caller-supplied set of granted permissions against what the skill
    declares it needs. Wiring granted_permissions to a real session or
    identity/trust source is a separate, future integration.
    """

    def __init__(self, registry: SkillRegistry) -> None:
        self.registry = registry

    def is_authorized(
        self,
        skill_id: str,
        granted_permissions: FrozenSet[str],
    ) -> bool:
        """
        Check whether granted_permissions satisfies the skill's
        required_permissions. Fails closed for unknown skills.
        """
        manifest = self.registry.get_manifest(skill_id)

        if manifest is None:
            logger.warning("Authorization denied: unknown skill_id=%s", skill_id)
            return False

        missing = set(manifest.required_permissions) - set(granted_permissions)

        if missing:
            logger.warning(
                "Authorization denied for skill_id=%s: missing permissions=%s",
                skill_id,
                sorted(missing),
            )
            return False

        return True

    def get_authorized_handler(
        self,
        skill_id: str,
        granted_permissions: FrozenSet[str],
    ) -> Callable[..., object]:
        """
        Return the skill's handler only if fully authorized.

        Raises SkillAuthorizationError otherwise. This is the only
        method that should ever be used to obtain a handler meant to
        actually run.
        """
        if not self.is_authorized(skill_id, granted_permissions):
            raise SkillAuthorizationError(
                f"Skill '{skill_id}' is not authorized for the granted permissions."
            )

        handler = self.registry.get_handler(skill_id)

        if handler is None:
            # Should be unreachable if is_authorized passed, but fail
            # closed defensively rather than assume.
            raise SkillAuthorizationError(
                f"Skill '{skill_id}' has no registered handler."
            )

        logger.info("Authorized handler released for skill_id=%s", skill_id)
        return handler


__all__ = [
    "SkillAuthorizationGate",
    "SkillAuthorizationError",
]
