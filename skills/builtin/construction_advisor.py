"""
NEXA Africa Operating System
File: skills/builtin/construction_advisor.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Builtin skill providing general, safety-first construction
             reference guidance from a small curated table. This is
             general information only, never a substitute for a licensed
             engineer or contractor — the response says so explicitly.
             Data is static and human-curated, not generated, since
             incorrect structural guidance can cause real harm.
"""

from __future__ import annotations

from typing import Any, Dict

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry

CONSTRUCTION_ADVISOR_SKILL = SkillManifest(
    skill_id="construction.reference_advisor",
    name="Construction Reference Advisor",
    description="Provides general, safety-first reference guidance for common construction topics.",
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)

_TOPIC_GUIDANCE: Dict[str, Dict[str, Any]] = {
    "foundation": {
        "common_names": ["foundation", "footing"],
        "summary": (
            "Foundation type and depth depend heavily on local soil "
            "conditions, water table, and building load — these must be "
            "assessed on site, not assumed from general guidance."
        ),
        "key_safety_point": (
            "Never dig a foundation trench deeper than about 1.2m without "
            "proper shoring; unsupported trench walls can collapse without warning."
        ),
    },
    "roofing": {
        "common_names": ["roofing", "roof"],
        "summary": (
            "Roof pitch, material choice, and drainage should account for local rainfall intensity and wind conditions."
        ),
        "key_safety_point": (
            "Roof work is a leading cause of construction falls. Use proper "
            "fall-arrest equipment and never work on a wet or unstable roof surface."
        ),
    },
    "scaffolding": {
        "common_names": ["scaffolding", "scaffold"],
        "summary": ("Scaffolding must be erected on stable, level ground and inspected before each use."),
        "key_safety_point": (
            "Never exceed the scaffold's rated load capacity, and never use damaged or improvised scaffold components."
        ),
    },
    "block_work": {
        "common_names": ["block work", "blockwork", "masonry", "brickwork"],
        "summary": (
            "Proper mortar mix ratios and curing time are essential for "
            "wall strength — rushing curing time weakens the structure."
        ),
        "key_safety_point": (
            "Freshly laid block walls above about 1.5m need temporary "
            "bracing until mortar has cured; unbraced walls can topple."
        ),
    },
}

_DISCLAIMER = (
    "This is general safety-oriented reference information only, not "
    "engineering advice. Always consult a licensed engineer or contractor "
    "for actual structural decisions on your specific site."
)


def _construction_advisor_handler(topic: str) -> Dict[str, Any]:
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
    registry.register(CONSTRUCTION_ADVISOR_SKILL, _construction_advisor_handler)


__all__ = [
    "CONSTRUCTION_ADVISOR_SKILL",
    "register_builtin_skills",
]
