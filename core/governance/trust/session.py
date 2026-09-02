"""
NEXA Africa Operating System
File: core/governance/trust/session.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Resolves an identity into a TrustSession (a set of granted
             roles), isolating identity lookup to the trust layer.
             Authorization policy (core/execution/authorization/policy.py)
             consumes only the resulting granted_roles, never the
             identity itself. This is the boundary implementing
             "identity is not authorization."
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet

from core.identity.profile.identity_manager import global_identity_manager
from core.services.logging.logger import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class TrustSession:
    """
    Represents what an identity was found to be granted, at the moment
    of resolution. Authorization policy should reason only about
    granted_roles, never identity_id.
    """

    identity_id: str
    granted_roles: FrozenSet[str]


def resolve_trust_session(identity_id: str, requested_intent: str) -> TrustSession:
    """
    The only place identity_manager is consulted for authorization
    purposes. Determines which role the requested intent requires,
    checks it against the identity manager, and returns a TrustSession
    describing what was actually granted.
    """
    required_role = "CONSTITUTIONAL_FOUNDER" if "SYSTEM" in requested_intent else "INTERFACE_NODE"

    report = global_identity_manager.validate_access_rights(identity_id, required_role)
    authorized = bool(report["authorized"])

    granted = frozenset({required_role}) if authorized else frozenset()

    logger.info(
        "Trust session resolved for identity_id=%s intent=%s granted=%s",
        identity_id,
        requested_intent,
        sorted(granted),
    )

    return TrustSession(identity_id=identity_id, granted_roles=granted)


__all__ = [
    "TrustSession",
    "resolve_trust_session",
]
