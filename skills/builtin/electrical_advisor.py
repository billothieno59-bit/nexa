"""
NEXA Africa Operating System
File: skills/builtin/electrical_advisor.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Builtin skill providing general, safety-first electrical
             reference guidance from a small curated table. This is
             general information only, never a substitute for a licensed
             electrician — the response says so explicitly and never
             provides step-by-step live-wiring instructions, since
             incorrect electrical work can kill.
"""

from __future__ import annotations

from typing import Any, Dict

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry

ELECTRICAL_ADVISOR_SKILL = SkillManifest(
    skill_id="electrical.reference_advisor",
    name="Electrical Reference Advisor",
    description="Provides general, safety-first reference guidance for common electrical topics.",
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)

_TOPIC_GUIDANCE: Dict[str, Dict[str, Any]] = {
    "circuit_breaker": {
        "common_names": ["circuit breaker", "breaker", "fuse box", "consumer unit"],
        "summary": (
            "A circuit breaker automatically cuts power when current exceeds "
            "a safe threshold, protecting wiring from overheating."
        ),
        "key_safety_point": (
            "Never bypass, oversize, or tamper with a circuit breaker's rating — "
            "this is a fire hazard. Replacement must match the original rating."
        ),
    },
    "earthing": {
        "common_names": ["earthing", "grounding", "earth wire"],
        "summary": (
            "Earthing (grounding) gives fault current a safe path to the "
            "ground instead of through a person who touches a faulty appliance."
        ),
        "key_safety_point": (
            "Never remove, disconnect, or ignore a missing earth connection "
            "on any fixed wiring or appliance — this is a serious shock and fire risk."
        ),
    },
    "solar_wiring": {
        "common_names": ["solar wiring", "pv wiring"],
        "summary": (
            "Solar PV systems carry DC voltage that remains live even when "
            "disconnected from the grid, as long as panels are exposed to light."
        ),
        "key_safety_point": (
            "Never assume a solar circuit is de-energized just because it's "
            "disconnected from the inverter — cover panels before working on wiring."
        ),
    },
    "wiring_general": {
        "common_names": ["wiring", "house wiring", "rewiring"],
        "summary": (
            "Household wiring must match the expected load and follow local "
            "electrical code for wire gauge, breaker sizing, and outlet spacing."
        ),
        "key_safety_point": (
            "Always assume a wire is live until confirmed otherwise with a "
            "proper tester, and always isolate power at the breaker before touching wiring."
        ),
    },
}

_DISCLAIMER = (
    "This is general safety-oriented reference information only, never "
    "instructions for performing electrical work yourself. Electrical work "
    "should always be done or verified by a licensed electrician — incorrect "
    "wiring can cause fire, injury, or death."
)


def _electrical_advisor_handler(topic: str) -> Dict[str, Any]:
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
    registry.register(ELECTRICAL_ADVISOR_SKILL, _electrical_advisor_handler)


__all__ = [
    "ELECTRICAL_ADVISOR_SKILL",
    "register_builtin_skills",
]
