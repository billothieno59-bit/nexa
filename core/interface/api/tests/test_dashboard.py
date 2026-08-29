from core.interface.api.dashboard import dashboard_status


def test_dashboard_status():
    result = dashboard_status()

    assert isinstance(result, dict)
    assert "status" in result
