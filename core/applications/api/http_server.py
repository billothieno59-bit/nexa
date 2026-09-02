"""
NEXA Africa Operating System
File: core/applications/api/http_server.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Minimal, deliberately narrow HTTP server.

             Routes:
             - GET /api/dashboard — returns dashboard_status().
             - GET /api/skills — lists only builtin (non-privileged)
               skills reachable via POST /api/skills/<skill_id>.
             - POST /api/skills/<skill_id> — executes a builtin skill
               via core/applications/api/web_skill_gateway.py. Never
               reaches privileged skills (generation.voice,
               generation.image, ai.reason, system.shutdown_nexa) —
               those require CONSTITUTIONAL_FOUNDER, which the fixed
               web client identity never has. Still passes through the
               full governed pipeline: rate limiting, trust session,
               authorization.
             - GET /, /style.css, /script.js — serves the static
               frontend files (project root index.html, style.css,
               script.js).

             Scope, on purpose:
             - No API keys, secrets, or env var values are ever placed
               in a response body.
             - Only three specific static files are served, by
               explicit route — not a broad static folder mount.
             - CORS is not configured. Same-origin only.
             - No authentication exists on this server at all. It is
               intended for local, same-machine use only. Do not
               expose this port to a network without adding real auth
               first — execution is now reachable, not just read-only
               dashboard data.
"""

from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, request, send_file

from core.applications.api.web_skill_gateway import (
    list_web_reachable_skills,
    run_web_skill,
)
from core.interface.api.dashboard import dashboard_status

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/api/dashboard")
    def get_dashboard():
        return jsonify(dashboard_status())

    @app.get("/api/skills")
    def get_skills():
        return jsonify(list_web_reachable_skills())

    @app.post("/api/skills/<skill_id>")
    def post_skill(skill_id: str):
        payload = request.get_json(silent=True) or {}
        if not isinstance(payload, dict):
            return jsonify({"status": "rejected", "message": "Request body must be a JSON object."}), 400

        result = run_web_skill(skill_id, **payload)

        http_status = 200 if result.status == "executed" else 403 if result.status == "denied" else 429 if result.status == "rate_limited" else 500

        return jsonify({
            "status": result.status,
            "skill_id": result.skill_id,
            "message": result.message,
            "result": result.result,
        }), http_status

    @app.get("/")
    def index():
        return send_file(PROJECT_ROOT / "index.html")

    @app.get("/style.css")
    def style():
        return send_file(PROJECT_ROOT / "style.css")

    @app.get("/script.js")
    def script():
        return send_file(PROJECT_ROOT / "script.js")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)


__all__ = [
    "create_app",
    "app",
]
