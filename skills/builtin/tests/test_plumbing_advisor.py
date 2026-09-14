"""
NEXA Builtin Skill Tests: plumbing.reference_advisor
"""

from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.builtin.plumbing_advisor import (
    register_builtin_skills,
    PLUMBING_ADVISOR_SKILL,
)


def make_registry():
    registry = SkillRegistry()
    register_builtin_skills(registry)
    return registry


def test_known_topic_returns_guidance():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("plumbing.reference_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="pipe_fitting")
    assert result["status"] == "found"
    assert "key_safety_point" in result["guidance"]
    assert "disclaimer" in result


def test_common_name_alias_resolves():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("plumbing.reference_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="geyser")
    assert result["status"] == "found"
    assert result["topic"] == "water_heater"


def test_unknown_topic_returns_available_list():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("plumbing.reference_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="submarine hull design")
    assert result["status"] == "not_found"
    assert "pipe_fitting" in result["available_topics"]


def test_requires_text_process_permission():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    assert gate.is_authorized("plumbing.reference_advisor", frozenset()) is False


def test_manifest_shape():
    assert PLUMBING_ADVISOR_SKILL.tier == "builtin"
    assert PLUMBING_ADVISOR_SKILL.required_permissions == ("TEXT.PROCESS",)
