"""
NEXA Skill Execution Handler Adapter Tests.
"""

from core.execution.orchestrator.planner.planner import PlanStep
from skills.registry.registry import SkillRegistry
from skills.registry.manifest import SkillManifest
from skills.registry.execution_handler_adapter import (
    SkillActionHandler,
    build_skill_action_handlers,
)


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


def test_skill_action_handler_action_name_matches_skill_id():
    registry = make_registry_with_open_skill()
    handler = SkillActionHandler("test.echo", registry)
    assert handler.action_name == "test.echo"


def test_skill_action_handler_invokes_through_execution_bridge():
    registry = make_registry_with_open_skill()
    handler = SkillActionHandler("test.echo", registry)

    step = PlanStep(
        action="test.echo",
        parameters={"caller_id": "tester", "requested_intent": "GENERAL.QUERY", "text": "hi"},
    )

    result = handler.handle(step)
    assert result.status == "executed"
    assert result.result == "HI"


def test_build_skill_action_handlers_creates_one_per_skill():
    registry = make_registry_with_open_skill()
    handlers = build_skill_action_handlers(registry)

    assert len(handlers) == 1
    assert handlers[0].action_name == "test.echo"
