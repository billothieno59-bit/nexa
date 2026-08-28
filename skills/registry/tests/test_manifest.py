"""
NEXA SkillManifest Tests.
"""

import pytest

from skills.registry.manifest import SkillManifest


def test_valid_manifest():
    manifest = SkillManifest(
        skill_id="translate.sw_en",
        name="Swahili-English Translation",
        description="Translates text between Swahili and English.",
        tier="builtin",
        required_permissions=("FILES.READ",),
    )
    assert manifest.skill_id == "translate.sw_en"
    assert manifest.required_permissions == ("FILES.READ",)


def test_rejects_empty_skill_id():
    with pytest.raises(ValueError):
        SkillManifest(skill_id="", name="x", description="x", tier="builtin")


def test_rejects_invalid_tier():
    with pytest.raises(ValueError):
        SkillManifest(skill_id="x", name="x", description="x", tier="not_a_real_tier")


def test_rejects_empty_permission_string():
    with pytest.raises(ValueError):
        SkillManifest(
            skill_id="x", name="x", description="x", tier="builtin",
            required_permissions=("",),
        )


def test_manifest_is_immutable():
    manifest = SkillManifest(skill_id="x", name="x", description="x", tier="builtin")
    with pytest.raises(Exception):
        manifest.name = "changed"
