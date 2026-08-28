"""
NEXA Africa Operating System
File: skills/registry/execution_bridge.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Connects a caller identity to real skill execution: resolves
             a TrustSession (core/governance/trust/session.py), derives
             granted skill permissions (trust_bridge.py), and only then
             authorizes and invokes a skill via SkillAuthorizationGate.
             This is the wiring that makes skills reachable by an
             identified caller, rather than skills and identity/trust
             being two disconnected systems.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from core.governance.trust.session import resolve_trust_session
from skills.registry.trust_bridge import permissions_for_trust_session
from skills.registry.registry import SkillRegistry, global_skill_registry
from skills.registry.authorization import SkillAuthorizationGate, SkillAuthorizationError
from core.services.logging.logger import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class SkillExecutionResult:
    """
    Result of an attempted skill invocation through the bridge.
    """

    status: str
    skill_id: str
    result: Optional[Any] = None
    message: str = ""


def invoke_skill(
    caller_id: str,
    skill_id: str,
    requested_intent: str,
    registry: Optional[SkillRegistry] = None,
    **kwargs: Any,
) -> SkillExecutionResult:
    """
    Resolve caller_id into a TrustSession, derive granted permissions,
    and invoke skill_id only if authorized. Fails closed at every step:
    unknown skill, insufficient permissions, or handler failure all
    produce a "denied"/"error" result rather than raising uncontrolled.
    """
    active_registry = registry or global_skill_registry

    trust_session = resolve_trust_session(caller_id, requested_intent)
    granted_permissions = permissions_for_trust_session(trust_session)

    gate = SkillAuthorizationGate(active_registry)

    try:
        handler = gate.get_authorized_handler(skill_id, granted_permissions)
    except SkillAuthorizationError as exc:
        logger.warning(
            "Skill invocation denied for caller_id=%s skill_id=%s: %s",
            caller_id, skill_id, exc,
        )
        return SkillExecutionResult(
            status="denied",
            skill_id=skill_id,
            message=str(exc),
        )

    try:
        result = handler(**kwargs)
    except Exception as exc:
        logger.exception(
            "Skill handler raised for caller_id=%s skill_id=%s", caller_id, skill_id,
        )
        return SkillExecutionResult(
            status="error",
            skill_id=skill_id,
            message=f"Skill handler failed: {exc}",
        )

    logger.info("Skill executed for caller_id=%s skill_id=%s", caller_id, skill_id)
    return SkillExecutionResult(
        status="executed",
        skill_id=skill_id,
        result=result,
        message="Skill executed successfully.",
    )


__all__ = [
    "SkillExecutionResult",
    "invoke_skill",
]
