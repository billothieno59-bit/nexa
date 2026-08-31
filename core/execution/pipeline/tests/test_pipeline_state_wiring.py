"""
NEXA Execution Pipeline — PipelineState Wiring Tests.

Confirms core/execution/state/pipeline_state.py's PIPELINE_STATE is
actually advanced by ExecutionPipeline.process(), not just sitting
unused. Uses the global PIPELINE_STATE (same instance the dashboard
would read from), resetting between assertions for isolation.
"""

from core.cognition.thinking.decision_engine import Decision
from core.execution.pipeline.pipeline import ExecutionPipeline
from core.execution.state.pipeline_state import PIPELINE_STATE


def test_informational_request_advances_state_to_executor():
    PIPELINE_STATE.reset()

    decision = Decision(
        decision_type="informational",
        intent="question",
        confidence=0.96,
        requires_confirmation=False,
        reason="No external side effect.",
    )

    ExecutionPipeline().process(decision)

    # Reached the final real stage, since this decision type flows
    # all the way through to the executor.
    assert PIPELINE_STATE.current_stage == "Executor"


def test_blocked_request_stops_state_at_dispatcher():
    PIPELINE_STATE.reset()

    decision = Decision(
        decision_type="blocked",
        intent="dangerous_request",
        confidence=1.0,
        requires_confirmation=False,
        reason="Request blocked by governance.",
    )

    ExecutionPipeline().process(decision)

    # Dispatcher is the last stage that actually ran before the
    # pipeline short-circuited — state must not claim it reached
    # Authorization or Executor, which never ran.
    assert PIPELINE_STATE.current_stage == "Dispatcher"


def test_confirmation_required_stops_state_at_dispatcher():
    PIPELINE_STATE.reset()

    decision = Decision(
        decision_type="confirmation_required",
        intent="request_action",
        confidence=1.0,
        requires_confirmation=True,
        reason="External side effect.",
    )

    ExecutionPipeline().process(decision)

    assert PIPELINE_STATE.current_stage == "Dispatcher"


def test_each_run_resets_state_from_prior_run():
    decision_ready = Decision(
        decision_type="informational",
        intent="question",
        confidence=0.96,
        requires_confirmation=False,
        reason="No external side effect.",
    )
    ExecutionPipeline().process(decision_ready)
    assert PIPELINE_STATE.current_stage == "Executor"

    decision_blocked = Decision(
        decision_type="blocked",
        intent="dangerous_request",
        confidence=1.0,
        requires_confirmation=False,
        reason="Request blocked by governance.",
    )
    ExecutionPipeline().process(decision_blocked)

    # A second run must reset state, not carry over "Executor" from
    # the previous unrelated request.
    assert PIPELINE_STATE.current_stage == "Dispatcher"
