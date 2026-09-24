"""
NEXA Africa Operating System
File: skills/builtin/welding_advisor.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Builtin skill providing general, safety-first welding
             reference guidance from a small curated table. This is
             general information only, never a substitute for certified
             welding training — the response says so explicitly. Data
             is static and human-curated, not generated, since incorrect
             welding guidance can cause burns, fire, fume exposure, or
             structural failure.
"""

from __future__ import annotations

from typing import Any, Dict

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry

WELDING_ADVISOR_SKILL = SkillManifest(
    skill_id="welding.reference_advisor",
    name="Welding Reference Advisor",
    description="Provides general, safety-first reference guidance for common welding topics.",
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)

_TOPIC_GUIDANCE: Dict[str, Dict[str, Any]] = {
    "arc_welding": {
        "common_names": ["arc welding", "stick welding", "smaw"],
        "summary": (
            "Arc welding requires matching electrode type and amperage to "
            "the base metal's thickness — the wrong setting causes poor "
            "penetration or burn-through."
        ),
        "key_safety_point": (
            "Always wear a properly rated auto-darkening welding helmet; "
            "arc flash can cause permanent eye damage in seconds, even "
            "from a brief unshielded glance."
        ),
    },
    "gas_welding": {
        "common_names": ["gas welding", "oxy-acetylene", "oxyfuel"],
        "summary": (
            "Oxy-acetylene setups need correctly matched regulators and "
            "hoses, and cylinders must always be secured upright."
        ),
        "key_safety_point": (
            "Never use oil or grease on oxygen fittings or regulators — "
            "the combination can ignite explosively on contact with "
            "pressurized oxygen."
        ),
    },
    "ventilation": {
        "common_names": ["ventilation", "fumes", "welding fumes"],
        "summary": (
            "Welding fumes contain metal particulates and gases that "
            "vary by base metal and coating — galvanized steel in "
            "particular releases zinc oxide fumes."
        ),
        "key_safety_point": (
            "Never weld galvanized or coated metal in an enclosed space "
            "without forced ventilation or a respirator — zinc fume "
            "exposure causes acute metal fume fever."
        ),
    },
    "fire_safety": {
        "common_names": ["fire safety", "sparks", "fire prevention"],
        "summary": (
            "Welding sparks can travel several meters and ignite "
            "flammable material long after the initial weld is finished."
        ),
        "key_safety_point": (
            "Clear the work area of flammable materials within at least "
            "10 meters, and keep a fire extinguisher on hand — many "
            "welding fires start after the welder has already left."
        ),
    },
}

_DISCLAIMER = (
    "This is general safety-oriented reference information only, not "
    "certified welding instruction. Always work under proper training "
    "and with correct personal protective equipment — welding involves "
    "serious burn, fire, and fume hazards."
)


def _welding_advisor_handler(topic: str) -> Dict[str, Any]:
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
    registry.register(WELDING_ADVISOR_SKILL, _welding_advisor_handler)


__all__ = [
    "WELDING_ADVISOR_SKILL",
    "register_builtin_skills",
]
