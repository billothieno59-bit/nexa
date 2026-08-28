"""
NEXA Africa Operating System
File: skills/builtin/education_advisor.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Builtin skill providing general study-technique reference
             guidance from a small curated table. General information
             only — these are widely-supported general learning
             strategies, not tailored educational or psychological advice.
"""

from __future__ import annotations

from typing import Any, Dict

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry

EDUCATION_ADVISOR_SKILL = SkillManifest(
    skill_id="education.study_advisor",
    name="Study Techniques Advisor",
    description="Provides general reference guidance on common study techniques.",
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)

_TOPIC_GUIDANCE: Dict[str, Dict[str, Any]] = {
    "spaced_repetition": {
        "common_names": ["spaced repetition", "spaced practice"],
        "summary": (
            "Reviewing material at increasing intervals over time improves "
            "long-term retention more than cramming it all at once."
        ),
        "tip": "Review new material after 1 day, then 3 days, then a week, then a month.",
    },
    "active_recall": {
        "common_names": ["active recall", "self-testing", "practice testing"],
        "summary": (
            "Actively trying to recall information (e.g. via flashcards or "
            "practice questions) is more effective than simply re-reading notes."
        ),
        "tip": "Close your notes and try to write down everything you remember before checking.",
    },
    "study_scheduling": {
        "common_names": ["study scheduling", "time management", "study plan"],
        "summary": (
            "Breaking study sessions into focused blocks with short breaks "
            "(e.g. 25-45 minutes of focus, then a break) tends to sustain "
            "concentration better than long unbroken sessions."
        ),
        "tip": "Start with your hardest subject first, while your focus is freshest.",
    },
}

_DISCLAIMER = (
    "These are general, widely-supported study techniques, not tailored "
    "educational or psychological advice for your specific situation."
)


def _education_advisor_handler(topic: str) -> Dict[str, Any]:
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
    registry.register(EDUCATION_ADVISOR_SKILL, _education_advisor_handler)


__all__ = [
    "EDUCATION_ADVISOR_SKILL",
    "register_builtin_skills",
]
