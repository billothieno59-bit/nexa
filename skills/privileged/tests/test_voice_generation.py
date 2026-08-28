"""
NEXA Voice Generation Skill Tests. No real network calls.
"""

from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.privileged.voice_generation import register_privileged_skills, GENERATE_VOICE_SKILL


def test_skill_requires_voice_generate_permission():
    registry = SkillRegistry()
    register_privileged_skills(registry)
    gate = SkillAuthorizationGate(registry)

    assert gate.is_authorized("generation.voice", frozenset()) is False
    assert gate.is_authorized("generation.voice", frozenset({"VOICE.GENERATE"})) is True


def test_skill_uses_local_provider_when_selected():
    registry = SkillRegistry()
    register_privileged_skills(registry)
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("generation.voice", frozenset({"VOICE.GENERATE"}))

    result = handler(text="hello", provider_name="nexa_local")
    assert result["status"] == "not_implemented"


def test_manifest_shape():
    assert GENERATE_VOICE_SKILL.tier == "privileged"
    assert GENERATE_VOICE_SKILL.required_permissions == ("VOICE.GENERATE",)
