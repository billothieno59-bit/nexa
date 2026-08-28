"""
NEXA Africa Operating System
File: skills/builtin/entrepreneurship_advisor.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Builtin skill providing general small-business reference
             guidance from a small curated table. General information
             only, not financial, legal, or tax advice.
"""

from __future__ import annotations

from typing import Any, Dict

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry

ENTREPRENEURSHIP_ADVISOR_SKILL = SkillManifest(
    skill_id="entrepreneurship.reference_advisor",
    name="Entrepreneurship Reference Advisor",
    description="Provides general reference guidance on common small-business topics.",
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)

_TOPIC_GUIDANCE: Dict[str, Dict[str, Any]] = {
    "business_registration": {
        "common_names": ["business registration", "business license", "registering a business"],
        "summary": (
            "Registration requirements vary significantly by country and "
            "business type (sole proprietorship, partnership, limited company)."
        ),
        "tip": "Check your local business registry or chamber of commerce for exact requirements.",
    },
    "cash_flow_management": {
        "common_names": ["cash flow", "cash flow management", "business finances"],
        "summary": (
            "Tracking money in and out separately from profit helps catch "
            "cash shortfalls before they become a crisis, since profit on "
            "paper doesn't always mean cash in hand."
        ),
        "tip": "Keep a simple daily or weekly log of what came in and what went out.",
    },
    "pricing_strategy": {
        "common_names": ["pricing strategy", "how to price", "setting prices"],
        "summary": (
            "Prices need to cover your costs (materials, time, overhead) plus "
            "a margin, while staying competitive with what similar businesses charge locally."
        ),
        "tip": "Calculate your true cost per unit before setting a price, including your own time.",
    },
}

_DISCLAIMER = (
    "This is general reference information only, not financial, legal, or "
    "tax advice. Consult a qualified local advisor or your business registry "
    "for guidance specific to your situation."
)


def _entrepreneurship_advisor_handler(topic: str) -> Dict[str, Any]:
    normalized = topic.strip().lower()

    for key, info in _TOPIC_GUIDANCE.items():
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
        "available_topics": list(_TOPIC_GUIDANCE.keys()),
        "disclaimer": _DISCLAIMER,
    }


def register_builtin_skills(registry: SkillRegistry) -> None:
    registry.register(ENTREPRENEURSHIP_ADVISOR_SKILL, _entrepreneurship_advisor_handler)


__all__ = [
    "ENTREPRENEURSHIP_ADVISOR_SKILL",
    "register_builtin_skills",
]
