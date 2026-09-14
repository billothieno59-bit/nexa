"""
NEXA Africa Operating System
File: skills/builtin/plumbing_advisor.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Builtin skill providing general, safety-first plumbing
             reference guidance from a small curated table. This is
             general information only, never a substitute for a licensed
             plumber — the response says so explicitly. Data is static
             and human-curated, not generated, since incorrect plumbing
             guidance can cause water damage, contamination, or gas/
             sewage hazards.
"""

from __future__ import annotations

from typing import Any, Dict

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry

PLUMBING_ADVISOR_SKILL = SkillManifest(
    skill_id="plumbing.reference_advisor",
    name="Plumbing Reference Advisor",
    description="Provides general, safety-first reference guidance for common plumbing topics.",
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)

_TOPIC_GUIDANCE: Dict[str, Dict[str, Any]] = {
    "pipe_fitting": {
        "common_names": ["pipe fitting", "piping", "pipe joints"],
        "summary": (
            "Pipe material (PVC, copper, galvanized steel) determines the correct "
            "joining method — solvent weld, soldering, or threading — and mixing "
            "incompatible materials directly can cause leaks or corrosion."
        ),
        "key_safety_point": (
            "Never solder copper pipe that still contains water or gas; "
            "residual moisture can cause the joint to fail, and any gas "
            "line work should only be done with the supply fully isolated."
        ),
    },
    "drainage": {
        "common_names": ["drainage", "drains", "waste pipes"],
        "summary": (
            "Drain pipes need adequate fall (slope) toward the outlet, and "
            "each fixture typically needs a trap to prevent sewer gas from "
            "entering the building."
        ),
        "key_safety_point": (
            "Never remove or bypass a P-trap — sewer gas buildup indoors "
            "is a genuine health and, in some cases, explosion hazard."
        ),
    },
    "water_heater": {
        "common_names": ["water heater", "geyser", "hot water system"],
        "summary": (
            "Water heaters need a properly rated pressure relief valve and "
            "correct electrical or gas supply sizing for the unit's rating."
        ),
        "key_safety_point": (
            "Never cap, block, or remove a water heater's pressure relief "
            "valve — without it, a malfunctioning unit can build enough "
            "pressure to rupture violently."
        ),
    },
    "leak_repair": {
        "common_names": ["leak repair", "leak", "burst pipe"],
        "summary": (
            "Before repairing any leak, the affected section's water supply "
            "should be isolated at the nearest shutoff valve, not just the mains."
        ),
        "key_safety_point": (
            "If a leak is near any electrical wiring or outlet, shut off "
            "power to that circuit before doing any work — water and "
            "live electricity together are a serious shock hazard."
        ),
    },
}

_DISCLAIMER = (
    "This is general safety-oriented reference information only, not "
    "professional plumbing advice. Always consult a licensed plumber "
    "for actual work on your specific system, especially anything "
    "involving gas lines or a building's main water supply."
)


def _plumbing_advisor_handler(topic: str) -> Dict[str, Any]:
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
    registry.register(PLUMBING_ADVISOR_SKILL, _plumbing_advisor_handler)


__all__ = [
    "PLUMBING_ADVISOR_SKILL",
    "register_builtin_skills",
]
