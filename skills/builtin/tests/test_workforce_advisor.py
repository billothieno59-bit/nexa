"""
NEXA Builtin Skill Tests: workforce.reference_advisor
"""

from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.builtin.workforce_advisor import (
    register_builtin_skills,
    WORKFORCE_ADVISOR_SKILL,
)


def make_registry():
    registry = SkillRegistry()
    register_builtin_skills(registry)
    return registry


def test_known_topic_returns_guidance():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("workforce.reference_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="cv_writing")
    assert result["status"] == "found"
    assert "tip" in result["guidance"]
    assert "disclaimer" in result


def test_common_name_alias_resolves():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("workforce.reference_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="resume")
    assert result["status"] == "found"
    assert result["topic"] == "cv_writing"


def test_unknown_topic_returns_available_list():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("workforce.reference_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="astronaut recruitment")
    assert result["status"] == "not_found"
    assert "cv_writing" in result["available_topics"]


def test_requires_text_process_permission():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    assert gate.is_authorized("workforce.reference_advisor", frozenset()) is False


def test_manifest_shape():
    assert WORKFORCE_ADVISOR_SKILL.tier == "builtin"
    assert WORKFORCE_ADVISOR_SKILL.required_permissions == ("TEXT.PROCESS",)
