"""
NEXA Africa Operating System
File: skills/builtin/mechanics_advisor.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Builtin skill providing general, safety-first vehicle/
             engine mechanics reference guidance from a small curated
             table. This is general information only, never a
             substitute for a qualified mechanic — the response says
             so explicitly. Data is static and human-curated, not
             generated, since incorrect mechanical guidance can cause
             injury or vehicle failure.
"""

from __future__ import annotations

from typing import Any, Dict

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry

MECHANICS_ADVISOR_SKILL = SkillManifest(
    skill_id="mechanics.reference_advisor",
    name="Mechanics Reference Advisor",
    description="Provides general, safety-first reference guidance for common vehicle and engine mechanics topics.",
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)

_TOPIC_GUIDANCE: Dict[str, Dict[str, Any]] = {
    "brakes": {
        "common_names": ["brakes", "brake system", "braking"],
        "summary": (
            "Brake pad and fluid condition should be checked regularly — "
            "worn pads reduce stopping distance, and old brake fluid "
            "absorbs moisture that lowers its boiling point."
        ),
        "key_safety_point": (
            "Never drive with a spongy or sinking brake pedal — this "
            "usually means air or moisture has entered the brake lines, "
            "and brake failure can occur without further warning."
        ),
    },
    "jacking": {
        "common_names": ["jacking", "jack stand", "lifting vehicle"],
        "summary": (
            "A hydraulic jack lifts the vehicle but is not rated to hold "
            "it — jack stands rated for the vehicle's weight must always "
            "support the load before working underneath."
        ),
        "key_safety_point": (
            "Never work under a vehicle supported only by a jack — jacks "
            "can fail or slip, and a vehicle falling on someone "
            "underneath is frequently fatal."
        ),
    },
    "battery": {
        "common_names": ["battery", "car battery", "jump start"],
        "summary": (
            "Lead-acid batteries produce hydrogen gas, especially during "
            "charging or jump-starting, and battery acid is corrosive."
        ),
        "key_safety_point": (
            "Always connect jump-start cables in the correct order "
            "(positive to positive first, negative to an unpainted "
            "metal ground last) — reversed polarity or a spark near the "
            "battery can cause it to explode."
        ),
    },
    "engine_overheating": {
        "common_names": ["engine overheating", "overheating", "coolant"],
        "summary": (
            "An overheating engine is usually caused by low coolant, a "
            "failed thermostat, or a blocked radiator, and continuing to "
            "drive can cause serious engine damage."
        ),
        "key_safety_point": (
            "Never open a hot radiator cap — pressurized coolant can "
            "erupt as scalding steam and liquid, causing severe burns. "
            "Let the engine cool fully first."
        ),
    },
}

_DISCLAIMER = (
    "This is general safety-oriented reference information only, not "
    "professional mechanical advice. Always consult a qualified mechanic "
    "for actual repairs — vehicle work involves real risks from moving "
    "parts, pressurized systems, and vehicle weight."
)


def _mechanics_advisor_handler(topic: str) -> Dict[str, Any]:
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
    registry.register(MECHANICS_ADVISOR_SKILL, _mechanics_advisor_handler)


__all__ = [
    "MECHANICS_ADVISOR_SKILL",
    "register_builtin_skills",
]
