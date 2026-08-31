"""
NEXA HTTP Server Tests.
"""

import pytest

from core.applications.api.http_server import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config.update({"TESTING": True})
    with app.test_client() as test_client:
        yield test_client


def test_dashboard_route_returns_200(client):
    response = client.get("/api/dashboard")
    assert response.status_code == 200


def test_dashboard_route_returns_real_dashboard_shape(client):
    response = client.get("/api/dashboard")
    data = response.get_json()

    assert data["status"] == "online"
    assert data["system"] == "NEXA"
    assert "skills" in data
    assert "providers" in data
    assert "pipeline" in data


def test_dashboard_route_never_leaks_api_key_values(client, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-secret-value-should-never-appear")
    response = client.get("/api/dashboard")
    body_text = response.get_data(as_text=True)

    assert "sk-secret-value-should-never-appear" not in body_text
    assert response.get_json()["providers"]["anthropic"] == "connected"


def test_post_to_dashboard_route_is_not_allowed(client):
    response = client.post("/api/dashboard")
    assert response.status_code == 405


def test_no_skill_execution_route_exists(client):
    """
    Confirms the server's routes are exactly what's intended — no
    accidental extra route that could reach invoke_skill() or any
    privileged skill over the network.
    """
    response = client.get("/api/skills/generation.voice")
    assert response.status_code == 404

    response = client.post("/api/execute")
    assert response.status_code == 404


def test_unknown_route_returns_404(client):
    response = client.get("/api/nonexistent")
    assert response.status_code == 404


def test_index_route_serves_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"NEXA" in response.data


def test_style_route_serves_css(client):
    response = client.get("/style.css")
    assert response.status_code == 200


def test_script_route_serves_js(client):
    response = client.get("/script.js")
    assert response.status_code == 200