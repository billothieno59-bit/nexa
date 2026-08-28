"""
NEXA Africa Operating System
File: skills/builtin/water_systems_advisor.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Builtin skill providing general, safety-first water systems
             reference guidance from a small curated table. General
             information only, never a substitute for a qualified water
             engineer or public health authority — incorrect water
             treatment guidance can cause real illness.
"""

from __future__ import annotations

from typing import Any, Dict

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry

WATER_SYSTEMS_ADVISOR_SKILL = SkillManifest(
    skill_id="water_systems.reference_advisor",
    name="Water Systems Reference Advisor",
    description="Provides general, safety-first reference guidance for common water systems topics.",
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)

_TOPIC_GUIDANCE: Dict[str, Dict[str, Any]] = {
    "borehole": {
        "common_names": ["borehole", "well", "water well"],
        "summary": (
            "Borehole depth and yield depend heavily on local geology and "
            "water table depth, which must be assessed by a hydrogeologist "
            "or licensed driller before drilling."
        ),
        "key_safety_point": (
            "Always have borehole water tested for bacterial and chemical "
            "contamination before drinking it, even after treatment."
        ),
    },
    "rainwater_harvesting": {
        "common_names": ["rainwater harvesting", "rainwater collection"],
        "summary": (
            "First-flush diverters improve harvested water quality by "
            "discarding the initial, most-contaminated runoff from a roof."
        ),
        "key_safety_point": (
            "Stored rainwater can harbor mosquito larvae and bacteria — "
            "storage tanks should be covered and periodically cleaned."
        ),
    },
    "water_treatment": {
        "common_names": ["water treatment", "water purification", "water filtration"],
        "summary": (
            "Common household treatment methods include boiling, chlorination, "
            "and filtration — each addresses different types of contamination."
        ),
        "key_safety_point": (
            "Boiling kills pathogens but does not remove chemical contaminants; "
            "chlorination dosing must be correct to be both safe and effective."
        ),
    },
}

_DISCLAIMER = (
    "This is general reference information only, not a substitute for water "
    "testing and guidance from a qualified water engineer or your local "
    "public health authority."
)


def _water_systems_advisor_handler(topic: str) -> Dict[str, Any]:
    normalized = topic.strip().lower()

    for key, info in _TOPIC_GUIDANCE.items():
        if normalized == key or normalized in info["common_names"]:
            return {
                "status": "found",
                "topic": key,
                "guidance": {
                    "summary": info["summary"],
                    "key_safety_point": info["key_safety_point"],
                },
                "disclaimer": _DISCLAIMER,
            }

    return {
        "status": "not_found",
        "topic": topic,
        "available_topics": list(_TOPIC_GUIDANCE.keys()),
        "disclaimer": _DISCLAIMER,
    }


def register_builtin_skills(registry: SkillRegistry) -> None:
    registry.register(WATER_SYSTEMS_ADVISOR_SKILL, _water_systems_advisor_handler)


__all__ = [
    "WATER_SYSTEMS_ADVISOR_SKILL",
    "register_builtin_skills",
]
