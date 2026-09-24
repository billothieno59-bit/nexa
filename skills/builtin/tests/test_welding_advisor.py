"""
NEXA Builtin Skill Tests: welding.reference_advisor
"""

from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.builtin.welding_advisor import (
    register_builtin_skills,
    WELDING_ADVISOR_SKILL,
)


def make_registry():
    registry = SkillRegistry()
    register_builtin_skills(registry)
    return registry


def test_known_topic_returns_guidance():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("welding.reference_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="arc_welding")
    assert result["status"] == "found"
    assert "key_safety_point" in result["guidance"]
    assert "disclaimer" in result


def test_common_name_alias_resolves():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("welding.reference_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="oxyfuel")
    assert result["status"] == "found"
    assert result["topic"] == "gas_welding"


def test_unknown_topic_returns_available_list():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("welding.reference_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="submarine hull design")
    assert result["status"] == "not_found"
    assert "arc_welding" in result["available_topics"]


def test_requires_text_process_permission():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    assert gate.is_authorized("welding.reference_advisor", frozenset()) is False


def test_manifest_shape():
    assert WELDING_ADVISOR_SKILL.tier == "builtin"
    assert WELDING_ADVISOR_SKILL.required_permissions == ("TEXT.PROCESS",)
