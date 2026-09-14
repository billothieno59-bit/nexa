"""
NEXA Builtin Skill Tests: digital.online_safety_advisor
"""

from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.builtin.digital_safety_advisor import (
    register_builtin_skills,
    DIGITAL_SAFETY_SKILL,
)


def make_registry():
    registry = SkillRegistry()
    register_builtin_skills(registry)
    return registry


def test_known_topic_returns_guidance():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("digital.online_safety_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="phishing")
    assert result["status"] == "found"
    assert "summary" in result["guidance"]
    assert "disclaimer" in result


def test_common_name_alias_resolves():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("digital.online_safety_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="open network")
    assert result["status"] == "found"
    assert result["topic"] == "public_wifi_safety"


def test_unknown_topic_returns_available_list():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("digital.online_safety_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="two_factor_hardware_keys")
    assert result["status"] == "not_found"
    assert "phishing" in result["available_topics"]


def test_case_insensitive_lookup():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("digital.online_safety_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="STRONG PASSWORD")
    assert result["status"] == "found"


def test_requires_text_process_permission():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)

    assert gate.is_authorized("digital.online_safety_advisor", frozenset()) is False


def test_manifest_shape():
    assert DIGITAL_SAFETY_SKILL.tier == "builtin"
    assert DIGITAL_SAFETY_SKILL.required_permissions == ("TEXT.PROCESS",)
