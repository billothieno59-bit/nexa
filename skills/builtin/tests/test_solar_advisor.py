"""
NEXA Builtin Skill Tests: solar.reference_advisor
"""

from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.builtin.solar_advisor import (
    register_builtin_skills,
    SOLAR_ADVISOR_SKILL,
)


def make_registry():
    registry = SkillRegistry()
    register_builtin_skills(registry)
    return registry


def test_known_topic_returns_guidance():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("solar.reference_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="battery_storage")
    assert result["status"] == "found"
    assert "key_safety_point" in result["guidance"]
    assert "disclaimer" in result


def test_common_name_alias_resolves():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("solar.reference_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="how many panels")
    assert result["status"] == "found"
    assert result["topic"] == "panel_sizing"


def test_unknown_topic_returns_available_list():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("solar.reference_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="nuclear reactor design")
    assert result["status"] == "not_found"
    assert "panel_sizing" in result["available_topics"]


def test_requires_text_process_permission():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    assert gate.is_authorized("solar.reference_advisor", frozenset()) is False


def test_manifest_shape():
    assert SOLAR_ADVISOR_SKILL.tier == "builtin"
    assert SOLAR_ADVISOR_SKILL.required_permissions == ("TEXT.PROCESS",)
