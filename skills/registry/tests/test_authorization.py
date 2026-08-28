"""
NEXA SkillAuthorizationGate Tests.
"""

import pytest

from skills.registry.registry import SkillRegistry
from skills.registry.manifest import SkillManifest
from skills.registry.authorization import (
    SkillAuthorizationGate,
    SkillAuthorizationError,
)


def make_registry_with_skill(required_permissions=("FILES.READ",)):
    registry = SkillRegistry()
    manifest = SkillManifest(
        skill_id="translate.sw_en",
        name="Translation",
        description="Translates text.",
        tier="builtin",
        required_permissions=required_permissions,
    )

    def handler(text):
        return text.upper()

    registry.register(manifest, handler)
    return registry, handler


def test_authorized_when_all_permissions_granted():
    registry, handler = make_registry_with_skill()
    gate = SkillAuthorizationGate(registry)

    assert gate.is_authorized("translate.sw_en", frozenset({"FILES.READ"})) is True

    resolved = gate.get_authorized_handler("translate.sw_en", frozenset({"FILES.READ"}))
    assert resolved is handler


def test_denied_when_permission_missing():
    registry, _ = make_registry_with_skill()
    gate = SkillAuthorizationGate(registry)

    assert gate.is_authorized("translate.sw_en", frozenset()) is False

    with pytest.raises(SkillAuthorizationError):
        gate.get_authorized_handler("translate.sw_en", frozenset())


def test_denied_for_unknown_skill_fails_closed():
    registry = SkillRegistry()
    gate = SkillAuthorizationGate(registry)

    assert gate.is_authorized("nonexistent", frozenset({"ANYTHING"})) is False

    with pytest.raises(SkillAuthorizationError):
        gate.get_authorized_handler("nonexistent", frozenset({"ANYTHING"}))


def test_extra_granted_permissions_do_not_matter():
    registry, handler = make_registry_with_skill(required_permissions=("FILES.READ",))
    gate = SkillAuthorizationGate(registry)

    resolved = gate.get_authorized_handler(
        "translate.sw_en", frozenset({"FILES.READ", "FILES.WRITE", "KERNEL.MANAGE"})
    )
    assert resolved is handler


def test_skill_with_no_required_permissions_is_authorized_with_empty_grant():
    registry, handler = make_registry_with_skill(required_permissions=())
    gate = SkillAuthorizationGate(registry)

    resolved = gate.get_authorized_handler("translate.sw_en", frozenset())
    assert resolved is handler
