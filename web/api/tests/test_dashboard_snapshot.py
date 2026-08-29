from web.api.dashboard import dashboard_snapshot


def test_dashboard_snapshot_delegates_to_real_dashboard():
    result = dashboard_snapshot()
    assert result["status"] == "online"
    assert result["system"] == "NEXA"
    assert "skills" in result
    assert "providers" in result