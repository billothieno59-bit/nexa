from core.interface.api.services.dashboard_service import get_dashboard


def test_dashboard_returns_system_snapshot():
    snapshot = get_dashboard()

    assert snapshot["system"] == "NEXA"
    assert snapshot["version"] == "3.2"
    assert snapshot["phase"] == "Phase 3"
    assert snapshot["active_stage"] == "Decision"


def test_dashboard_provider_count():
    snapshot = get_dashboard()

    assert len(snapshot["providers"]) == 4

    assert snapshot["providers"]["reasoning"]["name"] == "Anthropic"
    assert snapshot["providers"]["image"]["name"] == "OpenAI"
    assert snapshot["providers"]["voice"]["name"] == "ElevenLabs"
    assert snapshot["providers"]["local"]["name"] == "NEXA Local"
