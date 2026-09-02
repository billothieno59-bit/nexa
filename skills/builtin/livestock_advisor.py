"""
NEXA Africa Operating System
File: skills/builtin/livestock_advisor.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Builtin skill providing general livestock husbandry
             reference guidance from a small curated table. General
             information only, never a substitute for a veterinarian —
             incorrect livestock health guidance can cause real harm to
             animals and economic loss.
"""

from __future__ import annotations

from typing import Any, Dict

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry

LIVESTOCK_ADVISOR_SKILL = SkillManifest(
    skill_id="livestock.reference_advisor",
    name="Livestock Reference Advisor",
    description="Provides general reference guidance for common livestock husbandry topics.",
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)

_TOPIC_GUIDANCE: Dict[str, Dict[str, Any]] = {
    "poultry": {
        "common_names": ["poultry", "chickens", "chicken keeping"],
        "summary": (
            "Chickens need consistent access to clean water, balanced feed, and a predator-proof, well-ventilated coop."
        ),
        "key_safety_point": (
            "Sudden drops in egg production or lethargy across multiple birds "
            "can indicate disease — isolate affected birds and consult a vet promptly."
        ),
    },
    "dairy_cattle": {
        "common_names": ["dairy cattle", "dairy cows", "cattle"],
        "summary": ("Milk yield depends on consistent feeding schedule, water access, and regular milking intervals."),
        "key_safety_point": (
            "Mastitis (udder infection) can spread and reduce milk quality — "
            "check for swelling, heat, or abnormal milk regularly."
        ),
    },
    "goats": {
        "common_names": ["goats", "goat keeping"],
        "summary": (
            "Goats are browsers, not grazers, and do best with varied forage "
            "including shrubs and tree leaves, not just pasture grass."
        ),
        "key_safety_point": (
            "Goats are highly susceptible to internal parasites — regular "
            "deworming on a vet-recommended schedule is important."
        ),
    },
}

_DISCLAIMER = (
    "This is general husbandry reference information only, not veterinary "
    "advice. Always consult a qualified veterinarian for animal health concerns."
)


def _livestock_advisor_handler(topic: str) -> Dict[str, Any]:
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
    registry.register(LIVESTOCK_ADVISOR_SKILL, _livestock_advisor_handler)


__all__ = [
    "LIVESTOCK_ADVISOR_SKILL",
    "register_builtin_skills",
]
