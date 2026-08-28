"""
NEXA Builtin Skill Tests: entrepreneurship.reference_advisor
"""

from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.builtin.entrepreneurship_advisor import (
    register_builtin_skills,
    ENTREPRENEURSHIP_ADVISOR_SKILL,
)


def make_registry():
    registry = SkillRegistry()
    register_builtin_skills(registry)
    return registry


def test_known_topic_returns_guidance():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("entrepreneurship.reference_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="cash_flow_management")
    assert result["status"] == "found"
    assert "tip" in result["guidance"]
    assert "disclaimer" in result


def test_common_name_alias_resolves():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("entrepreneurship.reference_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="business finances")
    assert result["status"] == "found"
    assert result["topic"] == "cash_flow_management"


def test_unknown_topic_returns_available_list():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("entrepreneurship.reference_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="hostile takeover strategy")
    assert result["status"] == "not_found"
    assert "cash_flow_management" in result["available_topics"]


def test_requires_text_process_permission():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    assert gate.is_authorized("entrepreneurship.reference_advisor", frozenset()) is False


def test_manifest_shape():
    assert ENTREPRENEURSHIP_ADVISOR_SKILL.tier == "builtin"
    assert ENTREPRENEURSHIP_ADVISOR_SKILL.required_permissions == ("TEXT.PROCESS",)
