"""
NEXA Builtin Skill Tests: water_systems.reference_advisor
"""

from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.builtin.water_systems_advisor import (
    register_builtin_skills,
    WATER_SYSTEMS_ADVISOR_SKILL,
)


def make_registry():
    registry = SkillRegistry()
    register_builtin_skills(registry)
    return registry


def test_known_topic_returns_guidance():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("water_systems.reference_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="borehole")
    assert result["status"] == "found"
    assert "key_safety_point" in result["guidance"]
    assert "disclaimer" in result


def test_common_name_alias_resolves():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("water_systems.reference_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="well")
    assert result["status"] == "found"
    assert result["topic"] == "borehole"


def test_unknown_topic_returns_available_list():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("water_systems.reference_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="desalination plant design")
    assert result["status"] == "not_found"
    assert "borehole" in result["available_topics"]


def test_requires_text_process_permission():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    assert gate.is_authorized("water_systems.reference_advisor", frozenset()) is False


def test_manifest_shape():
    assert WATER_SYSTEMS_ADVISOR_SKILL.tier == "builtin"
    assert WATER_SYSTEMS_ADVISOR_SKILL.required_permissions == ("TEXT.PROCESS",)
