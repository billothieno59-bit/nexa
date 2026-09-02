"""
NEXA Skill Execution Bridge Tests.
"""

from skills.registry.registry import SkillRegistry
from skills.registry.manifest import SkillManifest
from skills.registry.execution_bridge import invoke_skill, SkillExecutionResult


def make_registry_with_open_skill():
    registry = SkillRegistry()
    manifest = SkillManifest(
        skill_id="test.echo",
        name="Echo",
        description="Echoes input.",
        tier="builtin",
        required_permissions=(),
    )

    def handler(text):
        return text.upper()

    registry.register(manifest, handler)
    return registry


def make_registry_with_locked_skill():
    registry = SkillRegistry()
    manifest = SkillManifest(
        skill_id="test.locked",
        name="Locked",
        description="Requires a permission nobody has.",
        tier="privileged",
        required_permissions=("NOBODY.HAS.THIS",),
    )
    registry.register(manifest, lambda: "should not run")
    return registry


def test_invoke_open_skill_succeeds():
    registry = make_registry_with_open_skill()
    result = invoke_skill(
        caller_id="anyone",
        skill_id="test.echo",
        requested_intent="GENERAL.QUERY",
        registry=registry,
        text="hello",
    )
    assert isinstance(result, SkillExecutionResult)
    assert result.status == "executed"
    assert result.result == "HELLO"


def test_invoke_locked_skill_denied():
    registry = make_registry_with_locked_skill()
    result = invoke_skill(
        caller_id="anyone",
        skill_id="test.locked",
        requested_intent="GENERAL.QUERY",
        registry=registry,
    )
    assert result.status == "denied"


def test_invoke_unknown_skill_denied():
    registry = make_registry_with_open_skill()
    result = invoke_skill(
        caller_id="anyone",
        skill_id="nonexistent",
        requested_intent="GENERAL.QUERY",
        registry=registry,
    )
    assert result.status == "denied"


def test_handler_exception_becomes_error_status():
    registry = SkillRegistry()
    manifest = SkillManifest(
        skill_id="test.broken",
        name="Broken",
        description="Raises.",
        tier="builtin",
        required_permissions=(),
    )

    def broken_handler():
        raise RuntimeError("boom")

    registry.register(manifest, broken_handler)

    result = invoke_skill(
        caller_id="anyone",
        skill_id="test.broken",
        requested_intent="GENERAL.QUERY",
        registry=registry,
    )
    assert result.status == "error"
    assert "boom" in result.message
