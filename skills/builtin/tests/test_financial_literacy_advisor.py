"""
NEXA Builtin Skill Tests: finance.literacy_advisor
"""

from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.builtin.financial_literacy_advisor import (
    register_builtin_skills,
    FINANCIAL_LITERACY_SKILL,
)


def make_registry():
    registry = SkillRegistry()
    register_builtin_skills(registry)
    return registry


def test_known_topic_returns_guidance():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("finance.literacy_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="savings")
    assert result["status"] == "found"
    assert "summary" in result["guidance"]
    assert "disclaimer" in result


def test_common_name_alias_resolves():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("finance.literacy_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="mpesa safety")
    assert result["status"] == "found"
    assert result["topic"] == "mobile_money_safety"


def test_unknown_topic_returns_available_list():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("finance.literacy_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="cryptocurrency")
    assert result["status"] == "not_found"
    assert "savings" in result["available_topics"]


def test_case_insensitive_lookup():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("finance.literacy_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="BUDGETING")
    assert result["status"] == "found"


def test_requires_text_process_permission():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)

    assert gate.is_authorized("finance.literacy_advisor", frozenset()) is False


def test_manifest_shape():
    assert FINANCIAL_LITERACY_SKILL.tier == "builtin"
    assert FINANCIAL_LITERACY_SKILL.required_permissions == ("TEXT.PROCESS",)
