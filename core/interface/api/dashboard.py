"""NEXA dashboard API."""

from __future__ import annotations


def dashboard_status() -> dict[str, str]:
    """Return the current basic NEXA dashboard status."""
    return {
        "status": "online",
        "system": "NEXA",
    }
