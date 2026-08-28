"""
NEXA Builtin Skill Tests: accessibility.simplify_text
"""

from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.builtin.accessibility_simplify import (
    register_builtin_skills,
    SIMPLIFY_TEXT_SKILL,
)


def test_skill_registers_and_runs_end_to_end():
    registry = SkillRegistry()
    register_builtin_skills(registry)

    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler(
        "accessibility.simplify_text", frozenset({"TEXT.PROCESS"})
    )

    result = handler("This is short.")
    assert result == "This is short."


def test_skill_denied_without_permission():
    registry = SkillRegistry()
    register_builtin_skills(registry)

    gate = SkillAuthorizationGate(registry)
    assert gate.is_authorized("accessibility.simplify_text", frozenset()) is False


def test_manifest_matches_expected_shape():
    assert SIMPLIFY_TEXT_SKILL.tier == "builtin"
    assert SIMPLIFY_TEXT_SKILL.required_permissions == ("TEXT.PROCESS",)
