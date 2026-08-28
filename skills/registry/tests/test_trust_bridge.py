"""
NEXA Skill Trust Bridge Tests.
"""

import pytest

from core.governance.trust.session import TrustSession
from skills.registry.trust_bridge import permissions_for_trust_session


def test_interface_node_gets_text_process_and_knowledge_read():
    session = TrustSession(identity_id="x", granted_roles=frozenset({"INTERFACE_NODE"}))
    permissions = permissions_for_trust_session(session)
    assert permissions == frozenset({"TEXT.PROCESS", "KNOWLEDGE.READ"})


def test_founder_gets_expanded_permissions():
    session = TrustSession(identity_id="x", granted_roles=frozenset({"CONSTITUTIONAL_FOUNDER"}))
    permissions = permissions_for_trust_session(session)
    assert "TEXT.PROCESS" in permissions
    assert "SYSTEM.SHUTDOWN" in permissions
    assert "KNOWLEDGE.WRITE" in permissions
    assert "KNOWLEDGE.READ" in permissions
    assert "AI.REASON" in permissions
    assert "IMAGE.GENERATE" in permissions
    assert "VOICE.GENERATE" in permissions


def test_interface_node_does_not_get_generation_permissions():
    session = TrustSession(identity_id="x", granted_roles=frozenset({"INTERFACE_NODE"}))
    permissions = permissions_for_trust_session(session)
    assert "AI.REASON" not in permissions
    assert "IMAGE.GENERATE" not in permissions
    assert "VOICE.GENERATE" not in permissions


def test_unrecognized_role_grants_nothing():
    session = TrustSession(identity_id="x", granted_roles=frozenset({"UNKNOWN_ROLE"}))
    permissions = permissions_for_trust_session(session)
    assert permissions == frozenset()


def test_empty_roles_grants_nothing():
    session = TrustSession(identity_id="x", granted_roles=frozenset())
    permissions = permissions_for_trust_session(session)
    assert permissions == frozenset()


def test_rejects_non_trust_session():
    with pytest.raises(TypeError):
        permissions_for_trust_session("not a session")
