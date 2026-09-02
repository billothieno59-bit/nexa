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


def test_get_skills_route_excludes_privileged(client):
    response = client.get("/api/skills")
    assert response.status_code == 200
    data = response.get_json()
    assert "generation.voice" not in data
    assert "agriculture.crop_advisor" in data


def test_post_skill_route_executes_builtin_skill(client):
    response = client.post(
        "/api/skills/knowledge.recall_fact",
        json={"subject": "nexa_http_smoke_test"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "executed"


def test_post_skill_route_denies_privileged_skill(client):
    response = client.post(
        "/api/skills/generation.voice",
        json={"text": "hello"},
    )
    assert response.status_code == 403
    data = response.get_json()
    assert data["status"] == "denied"


def test_post_skill_route_denies_shutdown(client):
    response = client.post(
        "/api/skills/system.shutdown_nexa",
        json={"provided_key": "anything"},
    )
    assert response.status_code == 403


def test_post_skill_route_rejects_non_json_body(client):
    response = client.post(
        "/api/skills/knowledge.recall_fact",
        data="not json",
        content_type="text/plain",
    )
    # Flask's silent=True get_json returns None for bad content-type,
    # which becomes {} — so this actually runs with no kwargs, which
    # knowledge.recall_fact rejects since subject is required.
    assert response.status_code in (400, 403, 500)
