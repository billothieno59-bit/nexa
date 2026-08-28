"""
NEXA Builtin Skill Tests: livestock.reference_advisor
"""

from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.builtin.livestock_advisor import (
    register_builtin_skills,
    LIVESTOCK_ADVISOR_SKILL,
)


def make_registry():
    registry = SkillRegistry()
    register_builtin_skills(registry)
    return registry


def test_known_topic_returns_guidance():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("livestock.reference_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="poultry")
    assert result["status"] == "found"
    assert "key_safety_point" in result["guidance"]
    assert "disclaimer" in result


def test_common_name_alias_resolves():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("livestock.reference_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="chickens")
    assert result["status"] == "found"
    assert result["topic"] == "poultry"


def test_unknown_topic_returns_available_list():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("livestock.reference_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="ostrich farming")
    assert result["status"] == "not_found"
    assert "poultry" in result["available_topics"]


def test_requires_text_process_permission():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    assert gate.is_authorized("livestock.reference_advisor", frozenset()) is False


def test_manifest_shape():
    assert LIVESTOCK_ADVISOR_SKILL.tier == "builtin"
    assert LIVESTOCK_ADVISOR_SKILL.required_permissions == ("TEXT.PROCESS",)
