"""
NEXA Privileged Skill Tests: system.shutdown_nexa

These tests use ShutdownController's default shutdown_callback (a no-op
lambda), so no real process exit ever occurs during testing.
"""

from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.privileged.system_shutdown import (
    register_privileged_skills,
    SYSTEM_SHUTDOWN_SKILL,
)


def test_skill_requires_system_shutdown_permission():
    registry = SkillRegistry()
    register_privileged_skills(registry)
    gate = SkillAuthorizationGate(registry)

    assert gate.is_authorized("system.shutdown_nexa", frozenset()) is False
    assert gate.is_authorized(
        "system.shutdown_nexa", frozenset({"SYSTEM.SHUTDOWN"})
    ) is True


def test_manifest_is_privileged_tier():
    assert SYSTEM_SHUTDOWN_SKILL.tier == "privileged"
    assert SYSTEM_SHUTDOWN_SKILL.required_permissions == ("SYSTEM.SHUTDOWN",)


def test_authorized_caller_still_needs_correct_key(monkeypatch):
    monkeypatch.delenv("NEXA_EMERGENCY_KEY", raising=False)

    registry = SkillRegistry()
    register_privileged_skills(registry)
    gate = SkillAuthorizationGate(registry)

    handler = gate.get_authorized_handler(
        "system.shutdown_nexa", frozenset({"SYSTEM.SHUTDOWN"})
    )

    result = handler("some_key")
    assert result.granted is False
