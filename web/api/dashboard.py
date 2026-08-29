"""
NEXA Africa Operating System
File: web/api/dashboard.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Thin wrapper delegating to core/interface/api/dashboard.py's
             dashboard_status(), the single real dashboard implementation.
             This file previously duplicated that logic (with a bug —
             calling a nonexistent SkillRegistry.manifests() method, and
             a hardcoded stale test count) instead of reusing it. Fixed
             to avoid two dashboards drifting out of sync.
"""

from __future__ import annotations

from typing import Any, Dict

from core.interface.api.dashboard import dashboard_status


def dashboard_snapshot() -> Dict[str, Any]:
    """
    Return the current dashboard status. Delegates entirely to
    core/interface/api/dashboard.py — no separate skill-counting or
    provider-checking logic here, so there is exactly one source of
    truth for dashboard data.
    """
    return dashboard_status()


__all__ = [
    "dashboard_snapshot",
]
