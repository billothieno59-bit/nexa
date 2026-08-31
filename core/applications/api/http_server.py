"""
NEXA Africa Operating System
File: core/applications/api/http_server.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Minimal, deliberately narrow HTTP server.

             Routes:
             - GET /api/dashboard — returns the same dashboard_status()
               every other part of NEXA already uses. No new data
               source, no duplication.
             - GET /, /style.css, /script.js — serves the existing
               static frontend files (project root index.html,
               style.css, script.js) so they can be opened same-origin
               and actually call /api/dashboard, instead of via
               file:// where no fetch to a Python backend is possible.

             Scope, on purpose, for a first safe slice:
             - GET only everywhere. No route accepts a body or
               mutates anything.
             - No skill execution is reachable from HTTP. Calling
               invoke_skill() over the network (rate limiting, trust
               sessions, authorization, and especially generation.voice
               which costs money per call) is a deliberately separate,
               later decision — not something this file does.
             - No API keys, secrets, or env var values are ever placed
               in a response body. dashboard_status()'s provider info
               is only "connected" / "not_configured" strings.
             - Only three specific files are served, by explicit route
               — not a broad static folder mount over the whole project
               root, which would risk exposing files like .venv,
               requirements.txt, or docs/ that were never meant to be
               web-reachable.
             - CORS is not configured. This server is same-origin only
               until a real CORS policy is a deliberate decision.
"""

from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, send_file

from core.interface.api.dashboard import dashboard_status

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/api/dashboard")
    def get_dashboard():
        return jsonify(dashboard_status())

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