"""
NEXA Image Generation Skill Tests. No real network calls.
"""

from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.privileged.image_generation import register_privileged_skills, GENERATE_IMAGE_SKILL


def test_skill_requires_image_generate_permission():
    registry = SkillRegistry()
    register_privileged_skills(registry)
    gate = SkillAuthorizationGate(registry)

    assert gate.is_authorized("generation.image", frozenset()) is False
    assert gate.is_authorized("generation.image", frozenset({"IMAGE.GENERATE"})) is True


def test_skill_uses_local_provider_when_selected():
    registry = SkillRegistry()
    register_privileged_skills(registry)
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("generation.image", frozenset({"IMAGE.GENERATE"}))

    result = handler(prompt="a bird", provider_name="nexa_local")
    assert result["status"] == "not_implemented"


def test_manifest_shape():
    assert GENERATE_IMAGE_SKILL.tier == "privileged"
    assert GENERATE_IMAGE_SKILL.required_permissions == ("IMAGE.GENERATE",)
