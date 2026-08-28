"""
NEXA Builtin Skill Tests: education.study_advisor
"""

from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.builtin.education_advisor import (
    register_builtin_skills,
    EDUCATION_ADVISOR_SKILL,
)


def make_registry():
    registry = SkillRegistry()
    register_builtin_skills(registry)
    return registry


def test_known_topic_returns_guidance():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("education.study_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="active_recall")
    assert result["status"] == "found"
    assert "tip" in result["guidance"]
    assert "disclaimer" in result


def test_common_name_alias_resolves():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("education.study_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="self-testing")
    assert result["status"] == "found"
    assert result["topic"] == "active_recall"


def test_unknown_topic_returns_available_list():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("education.study_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="quantum computing curriculum")
    assert result["status"] == "not_found"
    assert "active_recall" in result["available_topics"]


def test_requires_text_process_permission():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    assert gate.is_authorized("education.study_advisor", frozenset()) is False


def test_manifest_shape():
    assert EDUCATION_ADVISOR_SKILL.tier == "builtin"
    assert EDUCATION_ADVISOR_SKILL.required_permissions == ("TEXT.PROCESS",)
