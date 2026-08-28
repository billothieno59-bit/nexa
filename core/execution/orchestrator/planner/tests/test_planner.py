"""
NEXA Execution Planner Tests.

These tests verify that the execution planner:

- accepts canonical cognition decisions
- produces structured execution plans
- blocks blocked decisions
- prepares informational responses
- requires confirmation for external side effects
- safely handles unknown decision types
- does not execute external actions

The planner must remain a planning component only.
"""

from core.cognition.thinking.decision_engine import Decision
from core.execution.orchestrator.planner.planner import (
    ExecutionPlan,
    ExecutionPlanner,
    PlanStep,
)


def make_decision(
    decision_type: str,
    intent: str = "test_intent",
    confidence: float = 1.0,
    requires_confirmation: bool = False,
    reason: str = "Test decision.",
) -> Decision:
    """
    Create a canonical cognition Decision for testing.
    """

    return Decision(
        decision_type=decision_type,
        intent=intent,
        confidence=confidence,
        requires_confirmation=requires_confirmation,
        reason=reason,
    )


def test_planner_imports():
    """
    Verify the planner can be instantiated.
    """

    planner = ExecutionPlanner()

    assert isinstance(planner, ExecutionPlanner)


def test_blocked_decision_produces_blocked_plan():
    """
    A blocked cognitive decision must produce a blocked execution plan.
    """

    planner = ExecutionPlanner()

    decision = make_decision(
        decision_type="blocked",
        intent="dangerous_action",
        reason="Action is not permitted.",
    )

    plan = planner.create_plan(decision)

    assert isinstance(plan, ExecutionPlan)
    assert plan.status == "blocked"
    assert plan.intent == "dangerous_action"
    assert plan.requires_confirmation is False
    assert plan.steps == ()
    assert plan.reason == "Action is not permitted."


def test_informational_decision_produces_response_step():
    """
    An informational decision should produce a response plan.
    """

    planner = ExecutionPlanner()

    decision = make_decision(
        decision_type="informational",
        intent="ask_question",
        reason="Informational request.",
    )

    plan = planner.create_plan(decision)

    assert isinstance(plan, ExecutionPlan)
    assert plan.status == "ready"
    assert plan.intent == "ask_question"
    assert plan.requires_confirmation is False

    assert len(plan.steps) == 1

    step = plan.steps[0]

    assert isinstance(step, PlanStep)
    assert step.action == "respond"
    assert step.parameters["intent"] == "ask_question"


def test_confirmation_required_produces_confirmation_step():
    """
    A decision involving an external side effect must require confirmation.
    """

    planner = ExecutionPlanner()

    decision = make_decision(
        decision_type="confirmation_required",
        intent="request_action",
        confidence=1.0,
        requires_confirmation=True,
        reason="External side effect.",
    )

    plan = planner.create_plan(decision)

    assert isinstance(plan, ExecutionPlan)
    assert plan.status == "awaiting_confirmation"
    assert plan.intent == "request_action"
    assert plan.requires_confirmation is True
    assert len(plan.steps) == 1

    step = plan.steps[0]

    assert isinstance(step, PlanStep)
    assert step.action == "await_confirmation"
    assert step.parameters["intent"] == "request_action"
    assert plan.reason == "External side effect."


def test_unknown_decision_type_is_blocked():
    """
    Unknown decision types must fail safely closed.
    """

    planner = ExecutionPlanner()

    decision = make_decision(
        decision_type="unknown_decision_type",
        intent="unknown_action",
        reason="Unknown decision.",
    )

    plan = planner.create_plan(decision)

    assert isinstance(plan, ExecutionPlan)
    assert plan.status == "blocked"
    assert plan.intent == "unknown_action"
    assert plan.requires_confirmation is False
    assert plan.steps == ()
    assert plan.reason == "Unknown decision type."


def test_planner_does_not_execute_actions():
    """
    The planner must only describe actions.

    This test verifies that returned steps are data structures,
    not executable operations.
    """

    planner = ExecutionPlanner()

    decision = make_decision(
        decision_type="confirmation_required",
        intent="external_action",
        requires_confirmation=True,
        reason="External side effect.",
    )

    plan = planner.create_plan(decision)

    assert isinstance(plan.steps, tuple)

    for step in plan.steps:
        assert isinstance(step, PlanStep)
        assert isinstance(step.action, str)
        assert isinstance(step.parameters, dict)


def test_plan_steps_are_immutable():
    """
    PlanStep is defined as a frozen dataclass and should be immutable.
    """

    step = PlanStep(
        action="respond",
        parameters={"intent": "test"},
    )

    assert step.action == "respond"
    assert step.parameters["intent"] == "test"


def test_execution_plan_is_immutable():
    """
    ExecutionPlan is defined as a frozen dataclass and should be immutable.
    """

    plan = ExecutionPlan(
        status="ready",
        intent="test",
        requires_confirmation=False,
    )

    assert plan.status == "ready"
    assert plan.intent == "test"
    assert plan.requires_confirmation is False
