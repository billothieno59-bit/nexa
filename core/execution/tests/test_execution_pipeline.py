from core.cognition.thinking.decision_engine import Decision
from core.execution.pipeline.pipeline import (
    ExecutionPipeline,
    ExecutionPipelineResult,
)


def test_blocked_request_stops_at_dispatcher():
    decision = Decision(
        decision_type="blocked",
        intent="dangerous_request",
        confidence=1.0,
        requires_confirmation=False,
        reason="Request blocked by governance.",
    )

    result = ExecutionPipeline().process(decision)

    assert isinstance(result, ExecutionPipelineResult)
    assert result.plan.status == "blocked"
    assert result.orchestration.status == "blocked"
    assert result.dispatch.status == "blocked"
    assert result.execution.status == "blocked"
    assert result.execution.executed_steps == ()


def test_informational_request_reaches_ready_state():
    decision = Decision(
        decision_type="informational",
        intent="question",
        confidence=0.96,
        requires_confirmation=False,
        reason="No external side effect.",
    )

    result = ExecutionPipeline().process(decision)

    assert isinstance(result, ExecutionPipelineResult)
    assert result.plan.status == "ready"
    assert result.orchestration.status == "ready"
    assert result.dispatch.status == "ready_for_execution"
    assert result.execution.status == "accepted"
    assert result.execution.executed_steps == ()
    assert len(result.dispatch.steps) == 1
    assert result.dispatch.steps[0].action == "respond"


def test_confirmation_request_stops_before_execution():
    decision = Decision(
        decision_type="confirmation_required",
        intent="request_action",
        confidence=1.0,
        requires_confirmation=True,
        reason="External side effect.",
    )

    result = ExecutionPipeline().process(decision)

    assert isinstance(result, ExecutionPipelineResult)
    assert result.plan.status == "awaiting_confirmation"
    assert result.orchestration.status == "awaiting_confirmation"
    assert result.dispatch.status == "awaiting_confirmation"
    assert result.execution.status == "awaiting_confirmation"
    assert result.execution.executed_steps == ()


def test_unknown_decision_type_is_blocked_end_to_end():
    decision = Decision(
        decision_type="something_unknown",
        intent="unknown",
        confidence=1.0,
        requires_confirmation=False,
        reason="Test.",
    )

    result = ExecutionPipeline().process(decision)

    assert isinstance(result, ExecutionPipelineResult)
    assert result.plan.status == "blocked"
    assert result.orchestration.status == "blocked"
    assert result.dispatch.status == "blocked"
    assert result.execution.status == "blocked"
    assert result.execution.executed_steps == ()


def test_execution_pipeline_result_is_immutable():
    decision = Decision(
        decision_type="informational",
        intent="question",
        confidence=0.96,
        requires_confirmation=False,
        reason="No external side effect.",
    )

    result = ExecutionPipeline().process(decision)

    try:
        result.plan = result.plan
    except Exception:
        pass
    else:
        raise AssertionError("ExecutionPipelineResult must be immutable.")


def test_pipeline_rejects_invalid_decision():
    pipeline = ExecutionPipeline()

    try:
        pipeline.process("not-a-decision")
    except TypeError:
        pass
    else:
        raise AssertionError("ExecutionPipeline must reject invalid decisions.")


def test_pipeline_preserves_all_stage_results():
    decision = Decision(
        decision_type="informational",
        intent="question",
        confidence=0.96,
        requires_confirmation=False,
        reason="No external side effect.",
    )

    result = ExecutionPipeline().process(decision)

    assert result.plan is not None
    assert result.orchestration is not None
    assert result.dispatch is not None
    assert result.execution is not None


def test_pipeline_never_executes_steps():
    decision = Decision(
        decision_type="informational",
        intent="question",
        confidence=0.96,
        requires_confirmation=False,
        reason="No external side effect.",
    )

    result = ExecutionPipeline().process(decision)

    assert result.execution.executed_steps == ()
