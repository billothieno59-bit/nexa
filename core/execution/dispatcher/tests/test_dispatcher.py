from core.execution.dispatcher.dispatcher import ExecutionDispatcher
from core.execution.orchestrator.orchestrator import OrchestrationResult
from core.execution.orchestrator.planner.planner import PlanStep


def test_blocked_result_stays_blocked():
    result = OrchestrationResult(
        status="blocked",
        intent="dangerous_request",
        reason="Blocked by governance.",
    )

    dispatched = ExecutionDispatcher().dispatch(result)

    assert dispatched.status == "blocked"
    assert dispatched.intent == "dangerous_request"
    assert dispatched.steps == ()
    assert dispatched.reason == "Blocked by governance."


def test_confirmation_result_does_not_proceed():
    result = OrchestrationResult(
        status="awaiting_confirmation",
        intent="send_message",
        steps=(
            PlanStep(
                action="send_message",
                parameters={"recipient": "user"},
            ),
        ),
        reason="Confirmation required.",
    )

    dispatched = ExecutionDispatcher().dispatch(result)

    assert dispatched.status == "awaiting_confirmation"
    assert dispatched.intent == "send_message"
    assert dispatched.steps == ()
    assert dispatched.reason == "Execution requires confirmation."


def test_ready_result_is_ready_for_execution():
    result = OrchestrationResult(
        status="ready",
        intent="question",
        steps=(
            PlanStep(
                action="respond",
                parameters={"intent": "question"},
            ),
        ),
        reason="No external side effect.",
    )

    dispatched = ExecutionDispatcher().dispatch(result)

    assert dispatched.status == "ready_for_execution"
    assert dispatched.intent == "question"
    assert len(dispatched.steps) == 1
    assert dispatched.steps[0].action == "respond"


def test_unknown_status_is_blocked():
    result = OrchestrationResult(
        status="something_unknown",
        intent="test",
    )

    dispatched = ExecutionDispatcher().dispatch(result)

    assert dispatched.status == "blocked"
    assert dispatched.intent == "test"
    assert dispatched.steps == ()
    assert dispatched.reason == "Unknown orchestration result status."


def test_dispatcher_does_not_execute_actions():
    result = OrchestrationResult(
        status="ready",
        intent="external_action",
        steps=(
            PlanStep(
                action="external_action",
                parameters={"target": "test"},
            ),
        ),
    )

    dispatched = ExecutionDispatcher().dispatch(result)

    assert dispatched.status == "ready_for_execution"
    assert dispatched.steps[0].action == "external_action"
