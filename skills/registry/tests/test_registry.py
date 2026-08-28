"""
NEXA SkillRegistry Tests.
"""

import pytest

from skills.registry.registry import SkillRegistry, DuplicateSkillError
from skills.registry.manifest import SkillManifest


def make_manifest(skill_id="translate.sw_en"):
    return SkillManifest(
        skill_id=skill_id,
        name="Translation",
        description="Translates text.",
        tier="builtin",
        required_permissions=("FILES.READ",),
    )


def test_register_and_retrieve_manifest_and_handler():
    registry = SkillRegistry()
    manifest = make_manifest()

    def handler(text):
        return text.upper()

    registry.register(manifest, handler)

    assert registry.get_manifest("translate.sw_en") == manifest
    assert registry.get_handler("translate.sw_en") is handler


def test_duplicate_skill_id_rejected():
    registry = SkillRegistry()
    registry.register(make_manifest(), lambda: None)

    with pytest.raises(DuplicateSkillError):
        registry.register(make_manifest(), lambda: None)


def test_register_rejects_non_manifest():
    registry = SkillRegistry()
    with pytest.raises(TypeError):
        registry.register("not a manifest", lambda: None)


def test_register_rejects_non_callable_handler():
    registry = SkillRegistry()
    with pytest.raises(TypeError):
        registry.register(make_manifest(), "not callable")


def test_list_skill_ids():
    registry = SkillRegistry()
    registry.register(make_manifest("a"), lambda: None)
    registry.register(make_manifest("b"), lambda: None)

    assert set(registry.list_skill_ids()) == {"a", "b"}


def test_required_permissions_for_unknown_skill_returns_empty():
    registry = SkillRegistry()
    assert registry.required_permissions_for("nonexistent") == ()


def test_registry_never_invokes_handler():
    registry = SkillRegistry()
    calls = []

    def handler():
        calls.append("invoked")

    registry.register(make_manifest(), handler)
    registry.get_handler("translate.sw_en")

    assert calls == []
