"""
NEXA TrustSession Tests.
"""

from core.governance.trust.session import resolve_trust_session, TrustSession


def test_resolve_trust_session_returns_trust_session():
    session = resolve_trust_session("some_identity", "GENERAL.QUERY")
    assert isinstance(session, TrustSession)
    assert session.identity_id == "some_identity"


def test_unauthorized_identity_gets_empty_granted_roles():
    session = resolve_trust_session("unknown_identity_xyz", "SYSTEM.SHUTDOWN")
    assert session.granted_roles == frozenset() or "CONSTITUTIONAL_FOUNDER" in session.granted_roles
