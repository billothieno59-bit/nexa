"""
NEXA Builtin Skill Tests: agriculture.crop_advisor
"""

from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.builtin.agriculture_advisor import (
    register_builtin_skills,
    AGRICULTURE_ADVISOR_SKILL,
)


def make_registry():
    registry = SkillRegistry()
    register_builtin_skills(registry)
    return registry


def test_known_crop_returns_guidance():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler(
        "agriculture.crop_advisor", frozenset({"TEXT.PROCESS"})
    )

    result = handler(crop="maize")
    assert result["status"] == "found"
    assert "typical_planting_season" in result["guidance"]
    assert "disclaimer" in result


def test_common_name_alias_resolves():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler(
        "agriculture.crop_advisor", frozenset({"TEXT.PROCESS"})
    )

    result = handler(crop="corn")
    assert result["status"] == "found"
    assert result["crop"] == "maize"


def test_unknown_crop_returns_available_list():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler(
        "agriculture.crop_advisor", frozenset({"TEXT.PROCESS"})
    )

    result = handler(crop="dragonfruit")
    assert result["status"] == "not_found"
    assert "maize" in result["available_crops"]


def test_case_insensitive_lookup():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler(
        "agriculture.crop_advisor", frozenset({"TEXT.PROCESS"})
    )

    result = handler(crop="MAIZE")
    assert result["status"] == "found"


def test_requires_text_process_permission():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)

    assert gate.is_authorized("agriculture.crop_advisor", frozenset()) is False


def test_manifest_shape():
    assert AGRICULTURE_ADVISOR_SKILL.tier == "builtin"
    assert AGRICULTURE_ADVISOR_SKILL.required_permissions == ("TEXT.PROCESS",)
