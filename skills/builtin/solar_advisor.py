"""
NEXA Africa Operating System
File: skills/builtin/solar_advisor.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Builtin skill providing general, safety-first solar PV
             reference guidance from a small curated table. General
             information only — sizing and installation should be
             verified by a qualified solar installer.
"""

from __future__ import annotations

from typing import Any, Dict

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry

SOLAR_ADVISOR_SKILL = SkillManifest(
    skill_id="solar.reference_advisor",
    name="Solar Reference Advisor",
    description="Provides general, safety-first reference guidance for common solar PV topics.",
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)

_TOPIC_GUIDANCE: Dict[str, Dict[str, Any]] = {
    "panel_sizing": {
        "common_names": ["panel sizing", "system sizing", "how many panels"],
        "summary": (
            "Panel count depends on your daily energy usage (kWh), local sun "
            "hours, and panel wattage — a rough starting estimate is your "
            "daily kWh usage divided by (panel wattage x peak sun hours)."
        ),
        "key_safety_point": (
            "Always size the battery bank and inverter to match panel output; "
            "an undersized inverter can overheat under full panel load."
        ),
    },
    "battery_storage": {
        "common_names": ["battery storage", "battery bank", "solar battery"],
        "summary": (
            "Lead-acid batteries are cheaper but need more maintenance and "
            "have a shorter lifespan than lithium batteries, which cost more upfront."
        ),
        "key_safety_point": (
            "Batteries must be installed in a ventilated space — charging "
            "lead-acid batteries can release hydrogen gas, which is explosive in a confined space."
        ),
    },
    "installation": {
        "common_names": ["installation", "mounting"],
        "summary": (
            "Panels should be angled and oriented for maximum sun exposure "
            "based on your latitude, and mounted on a structure rated for wind load."
        ),
        "key_safety_point": (
            "Never work on panel wiring while panels are exposed to sunlight — "
            "they generate voltage as soon as they receive light, even disconnected from the system."
        ),
    },
}

_DISCLAIMER = (
    "This is general reference information only, not a substitute for a "
    "site assessment by a qualified solar installer, who can properly size "
    "your system for your actual usage and location."
)


def _solar_advisor_handler(topic: str) -> Dict[str, Any]:
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
    registry.register(SOLAR_ADVISOR_SKILL, _solar_advisor_handler)


__all__ = [
    "SOLAR_ADVISOR_SKILL",
    "register_builtin_skills",
]
