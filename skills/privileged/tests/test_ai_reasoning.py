"""
NEXA AI Reasoning Skill Tests. No real network calls.
"""

from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.privileged.ai_reasoning import register_privileged_skills, AI_REASON_SKILL


def test_skill_requires_ai_reason_permission():
    registry = SkillRegistry()
    register_privileged_skills(registry)
    gate = SkillAuthorizationGate(registry)

    assert gate.is_authorized("ai.reason", frozenset()) is False
    assert gate.is_authorized("ai.reason", frozenset({"AI.REASON"})) is True


def test_skill_uses_local_provider_when_selected():
    registry = SkillRegistry()
    register_privileged_skills(registry)
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("ai.reason", frozenset({"AI.REASON"}))

    result = handler(prompt="what is nexa", provider_name="nexa_local")
    assert result["status"] in ("ok", "not_found")


def test_manifest_shape():
    assert AI_REASON_SKILL.tier == "privileged"
    assert AI_REASON_SKILL.required_permissions == ("AI.REASON",)
