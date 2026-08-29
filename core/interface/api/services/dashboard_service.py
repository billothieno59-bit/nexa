

from __future__ import annotations

from typing import Any, Dict

from core.state.system_state import SYSTEM_STATE


def get_dashboard() -> Dict[str, Any]:
    """
    Canonical live dashboard endpoint.

    Returns the real System State snapshot so every frontend
    reads one source of truth.
    """
    return SYSTEM_STATE.snapshot()
