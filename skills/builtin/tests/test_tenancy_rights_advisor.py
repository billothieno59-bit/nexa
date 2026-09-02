"""
NEXA Builtin Skill Tests: housing.tenancy_rights_advisor
"""

from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.builtin.tenancy_rights_advisor import (
    register_builtin_skills,
    TENANCY_RIGHTS_SKILL,
)


def make_registry():
    registry = SkillRegistry()
    register_builtin_skills(registry)
    return registry


def test_known_topic_returns_guidance():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("housing.tenancy_rights_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="security_deposit")
    assert result["status"] == "found"
    assert "summary" in result["guidance"]
    assert "disclaimer" in result


def test_common_name_alias_resolves():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("housing.tenancy_rights_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="eviction notice")
    assert result["status"] == "found"
    assert result["topic"] == "notice_period"


def test_unknown_topic_returns_available_list():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("housing.tenancy_rights_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="subletting")
    assert result["status"] == "not_found"
    assert "security_deposit" in result["available_topics"]


def test_case_insensitive_lookup():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("housing.tenancy_rights_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="RENT INCREASE")
    assert result["status"] == "found"


def test_requires_text_process_permission():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)

    assert gate.is_authorized("housing.tenancy_rights_advisor", frozenset()) is False


def test_manifest_shape():
    assert TENANCY_RIGHTS_SKILL.tier == "builtin"
    assert TENANCY_RIGHTS_SKILL.required_permissions == ("TEXT.PROCESS",)
