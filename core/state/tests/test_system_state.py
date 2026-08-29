from core.state.system_state import SYSTEM_STATE, SystemState


def test_default_snapshot():
    snapshot = SYSTEM_STATE.snapshot()

    assert snapshot["system"] == "NEXA"
    assert snapshot["version"] == "3.2"
    assert snapshot["phase"] == "Phase 3"

    assert snapshot["providers"]["reasoning"]["name"] == "Anthropic"
    assert snapshot["providers"]["image"]["name"] == "OpenAI"
    assert snapshot["providers"]["voice"]["name"] == "ElevenLabs"
    assert snapshot["providers"]["local"]["status"] == "reserved"


def test_stage_changes():
    state = SystemState()

    state.set_stage("Planner")
    assert state.active_stage == "Planner"

    state.set_stage("Executor")
    assert state.active_stage == "Executor"
