"""
NEXA Africa Operating System
File: skills/builtin/health_advisor.py
Description: Builtin skill providing general health and prevention reference
             information from a curated table. General awareness only.
"""

from __future__ import annotations

from typing import Any, Dict

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry

HEALTH_ADVISOR_SKILL = SkillManifest(
    skill_id="health.primary_care_advisor",
    name="Primary Care Advisor",
    description="Provides general health-reference guidance on common wellness and safety topics.",
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)

_HEALTH_GUIDANCE: Dict[str, Dict[str, Any]] = {
    "fever": {
        "common_names": ["fever", "high temperature"],
        "summary": (
            "Fever is often a sign that the body is fighting an infection "
            "or inflammation, but it can also be caused by other factors."
        ),
        "tip": (
            "Rest, hydrate, and monitor temperature and symptoms closely; "
            "get professional care if the fever is severe or persistent."
        ),
    },
    "hydration": {
        "common_names": ["hydration", "dehydration", "water intake"],
        "summary": "Hydration supports normal body function, especially during heat, exercise, illness, or diarrhea.",
        "tip": "Sip fluids regularly and consider oral rehydration solutions if a person is losing fluids rapidly.",
    },
    "first_aid": {
        "common_names": ["first aid", "minor injury", "cuts", "wounds"],
        "summary": (
            "Basic first aid can reduce complications from minor cuts, "
            "scrapes, and burns by cleaning the area and protecting it."
        ),
        "tip": (
            "Wash hands before dressing a wound, clean gently, and seek "
            "proper medical attention for serious or deep injuries."
        ),
    },
}

_DISCLAIMER = (
    "This is general health information and is not a substitute for a "
    "licensed clinical professional or local emergency guidance."
)


def _health_advisor_handler(topic: str) -> Dict[str, Any]:
    normalized = topic.strip().lower()

    for key, info in _HEALTH_GUIDANCE.items():
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
        "available_topics": list(_HEALTH_GUIDANCE.keys()),
        "disclaimer": _DISCLAIMER,
    }


def register_builtin_skills(registry: SkillRegistry) -> None:
    registry.register(HEALTH_ADVISOR_SKILL, _health_advisor_handler)


__all__ = [
    "HEALTH_ADVISOR_SKILL",
    "register_builtin_skills",
]
