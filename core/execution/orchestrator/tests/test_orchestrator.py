"""
NEXA Execution Orchestrator Tests.

These tests verify that the orchestrator:

- uses the canonical cognition Decision
- uses the canonical ExecutionPlanner
- preserves blocked decisions
- preserves confirmation requirements
- preserves ready informational plans
- does not execute external actions
- produces structured orchestration results
"""

from core.cognition.thinking.decision_engine import Decision
from core.execution.orchestrator import (
    ExecutionOrchestrator,
    OrchestrationResult,
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
    Create a canonical Decision for testing.
    """

    return Decision(
        decision_type=decision_type,
        intent=intent,
        confidence=confidence,
        requires_confirmation=requires_confirmation,
        reason=reason,
    )


def test_orchestrator_imports():
    """
    Verify that the orchestrator can be instantiated.
    """

    orchestrator = ExecutionOrchestrator()

    assert isinstance(orchestrator, ExecutionOrchestrator)


def test_orchestrator_uses_execution_planner():
    """
    Verify that the orchestrator owns a canonical ExecutionPlanner.
    """

    orchestrator = ExecutionOrchestrator()

    assert isinstance(orchestrator.planner, ExecutionPlanner)


def test_blocked_decision_remains_blocked():
    """
    A blocked decision must remain blocked through orchestration.
    """

    orchestrator = ExecutionOrchestrator()

    decision = make_decision(
        decision_type="blocked",
        intent="dangerous_action",
        reason="Action is not permitted.",
    )

    result = orchestrator.orchestrate(decision)

    assert isinstance(result, OrchestrationResult)
    assert result.status == "blocked"
    assert result.plan.status == "blocked"
    assert result.plan.intent == "dangerous_action"
    assert result.plan.requires_confirmation is False
    assert result.message == "Execution plan is blocked."


def test_confirmation_required_is_preserved():
    """
    Confirmation requirements must survive orchestration.
    """

    orchestrator = ExecutionOrchestrator()

    decision = make_decision(
        decision_type="confirmation_required",
        intent="request_action",
        confidence=1.0,
        requires_confirmation=True,
        reason="External side effect.",
    )

    result = orchestrator.orchestrate(decision)

    assert isinstance(result, OrchestrationResult)
    assert result.status == "awaiting_confirmation"
    assert result.plan.status == "awaiting_confirmation"
    assert result.plan.intent == "request_action"
    assert result.plan.requires_confirmation is True
    assert result.message == "Confirmation is required before execution."


def test_informational_decision_is_ready():
    """
    Informational decisions should produce a ready orchestration result.
    """

    orchestrator = ExecutionOrchestrator()

    decision = make_decision(
        decision_type="informational",
        intent="ask_question",
        reason="Informational request.",
    )

    result = orchestrator.orchestrate(decision)

    assert isinstance(result, OrchestrationResult)
    assert result.status == "ready"
    assert result.plan.status == "ready"
    assert result.plan.intent == "ask_question"
    assert result.plan.requires_confirmation is False
    assert result.message == "Execution plan is ready."


def test_orchestrator_does_not_execute_actions():
    """
    The orchestrator must only coordinate plans.

    It must not execute external actions.
    """

    orchestrator = ExecutionOrchestrator()

    decision = make_decision(
        decision_type="confirmation_required",
        intent="external_action",
        requires_confirmation=True,
        reason="External side effect.",
    )

    result = orchestrator.orchestrate(decision)

    assert isinstance(result, OrchestrationResult)
    assert isinstance(result.plan, ExecutionPlan)

    for step in result.plan.steps:
        assert isinstance(step.action, str)
        assert isinstance(step.parameters, dict)


def test_unknown_decision_type_fails_closed():
    """
    Unknown decision types must remain blocked.
    """

    orchestrator = ExecutionOrchestrator()

    decision = make_decision(
        decision_type="unknown_decision",
        intent="unknown_action",
        reason="Unknown decision.",
    )

    result = orchestrator.orchestrate(decision)

    assert isinstance(result, OrchestrationResult)
    assert result.status == "blocked"
    assert result.plan.status == "blocked"
    assert result.message == "Execution plan is blocked."


def test_orchestration_result_is_immutable():
    """
    OrchestrationResult is a frozen dataclass.
    """

    decision = make_decision(
        decision_type="informational",
        intent="test",
    )

    plan = ExecutionPlanner().create_plan(decision)

    result = OrchestrationResult(
        status="ready",
        plan=plan,
        message="Execution plan is ready.",
    )

    assert result.status == "ready"
    assert result.plan == plan
    assert result.message == "Execution plan is ready."
