"""
NEXA Execution Layer Tests.
"""

import pytest

from core.cognition.thinking.decision_engine import Decision
from core.execution.executor import (
    ExecutionExecutor,
    ExecutionResult,
)
from core.execution.orchestrator.planner.planner import (
    ExecutionPlan,
    ExecutionPlanner,
)


def make_decision(
    decision_type: str,
    intent: str = "test_intent",
    confidence: float = 1.0,
    requires_confirmation: bool = False,
    reason: str = "Test decision.",
) -> Decision:
    """
    Create a canonical Decision.
    """

    return Decision(
        decision_type=decision_type,
        intent=intent,
        confidence=confidence,
        requires_confirmation=requires_confirmation,
        reason=reason,
    )


def make_plan(
    decision_type: str,
    intent: str = "test_intent",
    requires_confirmation: bool = False,
) -> ExecutionPlan:
    """
    Create an ExecutionPlan through the canonical planner.
    """

    decision = make_decision(
        decision_type=decision_type,
        intent=intent,
        requires_confirmation=requires_confirmation,
    )

    return ExecutionPlanner().create_plan(decision)


def test_executor_imports():
    """
    Executor must import and instantiate correctly.
    """

    executor = ExecutionExecutor()

    assert isinstance(executor, ExecutionExecutor)


def test_blocked_plan_is_never_executed():
    """
    Blocked plans must remain blocked.
    """

    executor = ExecutionExecutor()

    plan = make_plan(
        decision_type="blocked",
        intent="dangerous_action",
    )

    result = executor.execute(plan)

    assert isinstance(result, ExecutionResult)
    assert result.status == "blocked"
    assert result.plan == plan
    assert result.executed_steps == ()
    assert result.message == "Execution plan is blocked."


def test_confirmation_plan_is_never_executed():
    """
    Plans requiring confirmation must not execute.
    """

    executor = ExecutionExecutor()

    plan = make_plan(
        decision_type="confirmation_required",
        intent="external_action",
        requires_confirmation=True,
    )

    result = executor.execute(plan)

    assert isinstance(result, ExecutionResult)
    assert result.status == "awaiting_confirmation"
    assert result.plan == plan
    assert result.executed_steps == ()
    assert result.message == "Execution requires confirmation."


def test_ready_plan_is_accepted_without_side_effects():
    """
    Ready plans may cross the execution boundary,
    but no real external action is performed yet.
    """

    executor = ExecutionExecutor()

    plan = make_plan(
        decision_type="informational",
        intent="answer_question",
    )

    result = executor.execute(plan)

    assert isinstance(result, ExecutionResult)
    assert result.status == "accepted"
    assert result.plan == plan
    assert result.executed_steps == ()
    assert result.message == (
        "Execution plan accepted. "
        "No external action was performed."
    )


def test_unknown_plan_status_fails_closed():
    """
    Unknown states must never execute.
    """

    executor = ExecutionExecutor()

    plan = make_plan(
        decision_type="informational",
        intent="test",
    )

    object.__setattr__(plan, "status", "unknown")

    result = executor.execute(plan)

    assert result.status == "blocked"
    assert result.executed_steps == ()
    assert result.message == (
        "Unknown execution state. Failing closed."
    )


def test_invalid_input_is_rejected():
    """
    Executor must only accept ExecutionPlan objects.
    """

    executor = ExecutionExecutor()

    with pytest.raises(TypeError):
        executor.execute("not a plan")


def test_execution_result_is_immutable():
    """
    ExecutionResult must be immutable.
    """

    plan = make_plan(
        decision_type="informational",
        intent="test",
    )

    result = ExecutionResult(
        status="accepted",
        plan=plan,
        executed_steps=(),
        message="Accepted.",
    )

    with pytest.raises(Exception):
        result.status = "blocked"


def test_executor_does_not_execute_steps():
    """
    Even a ready plan must produce zero executed steps
    at this architectural stage.
    """

    executor = ExecutionExecutor()

    plan = make_plan(
        decision_type="informational",
        intent="future_action",
    )

    result = executor.execute(plan)

    assert result.executed_steps == ()
