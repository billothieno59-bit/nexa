"""
NEXA Africa Operating System
File: skills/builtin/climate_advisor.py
Description: Builtin skill providing general climate and adaptation guidance
             from a small curated table. General awareness only, not site-specific
             meteorological advice.
"""

from __future__ import annotations

from typing import Any, Dict

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry

CLIMATE_ADVISOR_SKILL = SkillManifest(
    skill_id="environment.climate_advisor",
    name="Climate Advisor",
    description="Provides general reference guidance on climate patterns and adaptation.",
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)

_CLIMATE_GUIDANCE: Dict[str, Dict[str, Any]] = {
    "drought": {
        "common_names": ["drought", "water stress", "dry spell"],
        "summary": "Drought reduces soil moisture and crop performance, so water conservation and soil cover become more important.",
        "tip": "Mulch the soil, reduce unnecessary irrigation, and store water where practical.",
    },
    "flooding": {
        "common_names": ["flooding", "heavy rain", "storm surge"],
        "summary": "Heavy rainfall can overwhelm drainage and damage crops, roads, and structures if water is not diverted early.",
        "tip": "Check drainage routes, protect low-lying areas, and move critical equipment to higher ground.",
    },
    "heat": {
        "common_names": ["heat", "extreme heat", "heatwave"],
        "summary": "High temperatures can increase water demand and stress on crops, livestock, and people.",
        "tip": "Schedule work in cooler hours and ensure shade, ventilation, and hydration are available.",
    },
}

_DISCLAIMER = "This is general climate awareness and adaptation guidance, not local metrological forecasting or site-specific engineering advice."


def _climate_advisor_handler(topic: str) -> Dict[str, Any]:
    normalized = topic.strip().lower()

    for key, info in _CLIMATE_GUIDANCE.items():
        if normalized == key or normalized in info["common_names"]:
            return {
                "status": "found",
                "topic": key,
                "guidance": {
                    "summary": info["summary"],
                    "tip": info["tip"],
                },
                "disclaimer": _DISCLAIMER,
            }

    return {
        "status": "not_found",
        "topic": topic,
        "available_topics": list(_CLIMATE_GUIDANCE.keys()),
        "disclaimer": _DISCLAIMER,
    }


def register_builtin_skills(registry: SkillRegistry) -> None:
    registry.register(CLIMATE_ADVISOR_SKILL, _climate_advisor_handler)


__all__ = [
    "CLIMATE_ADVISOR_SKILL",
    "register_builtin_skills",
]
