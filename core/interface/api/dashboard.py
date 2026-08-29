"""
NEXA Africa Operating System
File: core/interface/api/dashboard.py
Constitutional Owner: Bill Odhiambo Othieno
Description: NEXA dashboard API. Reports real, live system state
             (skill counts, configured providers) rather than static
             placeholder values.
"""

from __future__ import annotations

import os

from skills.registry.bootstrap import global_skill_registry

_PROVIDER_ENV_VARS = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "elevenlabs": "ELEVENLABS_API_KEY",
}


def _count_skills_by_tier() -> dict[str, int]:
    skill_ids = global_skill_registry.list_skill_ids()
    manifests = [global_skill_registry.get_manifest(skill_id) for skill_id in skill_ids]
    manifests = [m for m in manifests if m is not None]

    builtin_count = sum(1 for m in manifests if m.tier == "builtin")
    privileged_count = sum(1 for m in manifests if m.tier == "privileged")
    return {
        "builtin": builtin_count,
        "privileged": privileged_count,
        "total": len(manifests),
    }


def _provider_connection_status() -> dict[str, str]:
    return {
        name: "connected" if os.environ.get(env_var) else "not_configured"
        for name, env_var in _PROVIDER_ENV_VARS.items()
    }


def dashboard_status() -> dict[str, object]:
    """
    Return the current NEXA dashboard status, derived from real system
    state: actual registered skill counts and actual configured
    provider API keys — never hardcoded placeholder values.
    """
    return {
        "status": "online",
        "system": "NEXA",
        "skills": _count_skills_by_tier(),
        "providers": _provider_connection_status(),
    }


__all__ = [
    "dashboard_status",
]