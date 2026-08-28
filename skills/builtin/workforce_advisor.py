"""
NEXA Africa Operating System
File: skills/builtin/workforce_advisor.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Builtin skill providing general job-seeking and workplace
             reference guidance from a small curated table. General
             information only, not legal or career-counseling advice.
"""

from __future__ import annotations

from typing import Any, Dict

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry

WORKFORCE_ADVISOR_SKILL = SkillManifest(
    skill_id="workforce.reference_advisor",
    name="Workforce Reference Advisor",
    description="Provides general reference guidance on common job-seeking and workplace topics.",
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)

_TOPIC_GUIDANCE: Dict[str, Dict[str, Any]] = {
    "cv_writing": {
        "common_names": ["cv writing", "resume writing", "cv", "resume"],
        "summary": (
            "A strong CV highlights specific, measurable achievements rather "
            "than just listing job duties, and is tailored to each role you apply for."
        ),
        "tip": "Keep it to 1-2 pages and lead with your most relevant experience for the role.",
    },
    "interview_preparation": {
        "common_names": ["interview preparation", "interview prep", "job interview"],
        "summary": (
            "Researching the employer beforehand and preparing specific "
            "examples of past work (using a structured format like Situation-"
            "Task-Action-Result) helps you answer behavioral questions clearly."
        ),
        "tip": "Prepare 2-3 questions to ask the interviewer — it shows genuine interest.",
    },
    "workplace_rights": {
        "common_names": ["workplace rights", "labor rights", "employee rights"],
        "summary": (
            "Labor rights and protections vary significantly by country and "
            "region — general awareness helps, but specific situations need "
            "local verification."
        ),
        "tip": "Keep written records of any workplace disputes, including dates and details.",
    },
}

_DISCLAIMER = (
    "This is general reference information only, not legal advice or "
    "personalized career counseling. Labor laws vary by jurisdiction — "
    "consult a local labor office or qualified advisor for your specific situation."
)


def _workforce_advisor_handler(topic: str) -> Dict[str, Any]:
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
    registry.register(WORKFORCE_ADVISOR_SKILL, _workforce_advisor_handler)


__all__ = [
    "WORKFORCE_ADVISOR_SKILL",
    "register_builtin_skills",
]
