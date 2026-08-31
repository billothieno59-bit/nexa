"""
NEXA Africa Operating System
File: core/applications/api/http_server.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Minimal, deliberately narrow HTTP server. Exposes exactly
             one read-only route (GET /api/dashboard), returning the
             same dashboard_status() every other part of NEXA already
             uses — no new data source, no duplication.

             Scope, on purpose, for a first safe slice:
             - GET only. No route accepts a body or mutates anything.
             - No skill execution is reachable from HTTP. Calling
               invoke_skill() over the network (rate limiting, trust
               sessions, authorization, and especially generation.voice
               which costs money per call) is a deliberately separate,
               later decision — not something this file does.
             - No API keys, secrets, or env var values are ever placed
               in a response body. dashboard_status()'s provider info
               is only "connected" / "not_configured" strings.
             - CORS is not configured. This server is same-origin only
               until a real CORS policy is a deliberate decision.
"""

from __future__ import annotations

from flask import Flask, jsonify

from core.interface.api.dashboard import dashboard_status


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/api/dashboard")
    def get_dashboard():
        return jsonify(dashboard_status())

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)


__all__ = [
    "create_app",
    "app",
]
