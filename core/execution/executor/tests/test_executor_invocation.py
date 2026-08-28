"""
NEXA Execution Layer Invocation Tests.

Verifies that the executor actually invokes a handler when one is
registered for a step's action, while steps with no registered
handler remain side-effect-free exactly as before.
"""

from core.execution.executor.executor import ExecutionExecutor, ExecutionResult
from core.execution.executor.bootstrap import get_handler_registry
from core.execution.orchestrator.planner.planner import ExecutionPlan, PlanStep


def make_ready_plan(action: str) -> ExecutionPlan:
    """
    Build a minimal ready plan with a single step for the given action.
    """
    return ExecutionPlan(
        status="ready",
        intent="test_intent",
        requires_confirmation=False,
        steps=(PlanStep(action=action, parameters={}),),
        reason="Test plan.",
    )


def test_registered_handler_is_actually_invoked():
    """
    A step whose action matches a registered handler must be executed.
    """
    executor = ExecutionExecutor(registry=get_handler_registry())
    plan = make_ready_plan("INTENT_SYSTEM_DIAGNOSTIC_CHECK")

    result = executor.execute(plan)

    assert isinstance(result, ExecutionResult)
    assert result.status == "executed"
    assert len(result.executed_steps) == 1
    assert "INTENT_SYSTEM_DIAGNOSTIC_CHECK" in result.handler_results


def test_unregistered_action_is_still_accepted_without_execution():
    """
    A step with no registered handler must remain side-effect-free,
    exactly like the pre-invocation behavior.
    """
    executor = ExecutionExecutor(registry=get_handler_registry())
    plan = make_ready_plan("respond")

    result = executor.execute(plan)

    assert result.status == "accepted"
    assert result.executed_steps == ()
    assert result.handler_results == {}
