"""
NEXA Africa Operating System
File: skills/builtin/travel_advisor.py
Description: Builtin skill providing general travel and route-planning reference
             guidance from a curated table. General awareness only.
"""

from __future__ import annotations

from typing import Any, Dict

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry

TRAVEL_ADVISOR_SKILL = SkillManifest(
    skill_id="travel.route_advisor",
    name="Route Advisor",
    description="Provides general travel guidance on planning, weather, and preparedness.",
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)

_TRAVEL_GUIDANCE: Dict[str, Dict[str, Any]] = {
    "rain": {
        "common_names": ["rain", "rainy season", "wet season"],
        "summary": "Rain can affect roads, visibility, and travel times, so route planning should include extra delays and drainage checks.",
        "tip": "Allow extra time, inspect roads before departure, and avoid flooded areas or low crossings.",
    },
    "heat": {
        "common_names": ["heat", "hot weather", "sun exposure"],
        "summary": "Traveling in intense heat can increase fatigue and dehydration, especially for long distances or outdoor work.",
        "tip": "Carry water, rest in shaded areas, and avoid direct sun during the hottest periods of the day.",
    },
    "route_planning": {
        "common_names": ["route planning", "travel plan", "itinerary"],
        "summary": "Good route planning balances distance, road conditions, fuel availability, and backup options in case of delays.",
        "tip": "Have a primary and alternate route, keep emergency contacts ready, and confirm fuel or charging availability ahead of time.",
    },
}

_DISCLAIMER = "This is general route and travel guidance, not official transport, weather, or logistics advice for a particular route or authority."


def _travel_advisor_handler(topic: str) -> Dict[str, Any]:
    normalized = topic.strip().lower()

    for key, info in _TRAVEL_GUIDANCE.items():
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
        "available_topics": list(_TRAVEL_GUIDANCE.keys()),
        "disclaimer": _DISCLAIMER,
    }


def register_builtin_skills(registry: SkillRegistry) -> None:
    registry.register(TRAVEL_ADVISOR_SKILL, _travel_advisor_handler)


__all__ = [
    "TRAVEL_ADVISOR_SKILL",
    "register_builtin_skills",
]
