from __future__ import annotations

from typing import Any, Dict

from skills.registry.registry import SkillRegistry


def dashboard_snapshot(registry: SkillRegistry) -> Dict[str, Any]:
    builtin = 0
    privileged = 0

    for manifest in registry.manifests():
        if manifest.tier == "builtin":
            builtin += 1
        elif manifest.tier == "privileged":
            privileged += 1

    return {
        "system": "NEXA",
        "phase": "3.1",
        "tests": 364,
        "pipeline": [
            "Decision",
            "Planner",
            "Orchestrator",
            "Dispatcher",
            "Authorization",
            "Executor",
        ],
        "providers": {
            "reasoning": "Anthropic",
            "image": "OpenAI",
            "voice": "ElevenLabs",
            "local": "Reserved",
        },
        "skills": {
            "builtin": builtin,
            "privileged": privileged,
        },
    }