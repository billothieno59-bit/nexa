"""
NEXA Africa Operating System
File: skills/registry/trust_bridge.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Maps a TrustSession's granted_roles into the permission
             strings SkillAuthorizationGate understands. This is the
             piece that connects real identity/trust resolution
             (core/governance/trust/session.py) to skill authorization,
             replacing a caller-supplied permission set with one derived
             from an actual resolved identity.
"""

from __future__ import annotations

from typing import FrozenSet

from core.governance.trust.session import TrustSession

ROLE_PERMISSIONS = {
    "CONSTITUTIONAL_FOUNDER": frozenset({
        "TEXT.PROCESS",
        "KERNEL.MANAGE",
        "SYSTEM.SHUTDOWN",
        "KNOWLEDGE.WRITE",
        "KNOWLEDGE.READ",
        "AI.REASON",
        "IMAGE.GENERATE",
        "VOICE.GENERATE",
    }),
    "INTERFACE_NODE": frozenset({
        "TEXT.PROCESS",
        "KNOWLEDGE.READ",
    }),
}


def permissions_for_trust_session(session: TrustSession) -> FrozenSet[str]:
    """
    Derive the set of skill permissions granted by a TrustSession.

    A role with no entry in ROLE_PERMISSIONS grants nothing, per the
    fail-closed principle already used throughout this codebase.
    AI.REASON, IMAGE.GENERATE, and VOICE.GENERATE are deliberately
    granted only to CONSTITUTIONAL_FOUNDER — they cost money per call
    and send data to a third-party API.
    """
    if not isinstance(session, TrustSession):
        raise TypeError("permissions_for_trust_session() requires a TrustSession.")

    granted: set[str] = set()
    for role in session.granted_roles:
        granted |= ROLE_PERMISSIONS.get(role, frozenset())

    return frozenset(granted)


__all__ = [
    "permissions_for_trust_session",
    "ROLE_PERMISSIONS",
]
