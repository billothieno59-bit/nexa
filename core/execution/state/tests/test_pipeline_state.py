from core.execution.state.pipeline_state import PIPELINE_STATE, PipelineState


def test_default_stage():
    PIPELINE_STATE.reset()
    assert PIPELINE_STATE.current_stage == "Decision"


def test_pipeline_progression():
    state = PipelineState()

    assert state.current_stage == "Decision"

    state.next()
    assert state.current_stage == "Planner"

    state.next()
    assert state.current_stage == "Orchestrator"

    state.reset()
    assert state.current_stage == "Decision"


def test_snapshot():
    state = PipelineState()

    snap = state.snapshot()

    assert snap["current_stage"] == "Decision"
    assert snap["current_index"] == 0
    assert len(snap["stages"]) == 6
