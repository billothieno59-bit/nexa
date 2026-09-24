"""
NEXA Africa Operating System
File: skills/builtin/civic_services_advisor.py

Description:
    Builtin civic-services guidance skill.

    This module is intentionally self-contained. It provides general
    civic-services information and does not perform government actions,
    submit applications, make payments, or contact authorities.

    All real-world actions remain subject to the governed execution
    pipeline and authorization boundaries.
"""

from __future__ import annotations

from typing import Any

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry


CIVIC_SERVICES_SKILL = SkillManifest(
    skill_id="civic_services.advisor",
    name="Civic Services Advisor",
    description=(
        "Provides general guidance about civic services, public offices, "
        "documents, applications, and common government-service processes."
    ),
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)


def _normalize_query(query: Any) -> str:
    """
    Normalize the incoming civic-services query.

    The skill accepts ordinary text input. Invalid or empty input is
    converted into an empty string so the handler can fail safely.
    """
    if query is None:
        return ""

    if not isinstance(query, str):
        query = str(query)

    return " ".join(query.strip().split())


def _civic_services_handler(query: str) -> str:
    """
    Provide general civic-services guidance.

    This handler deliberately provides informational guidance only.
    It does not claim to know current requirements for a particular
    authority unless those requirements are supplied by the caller.
    """
    normalized = _normalize_query(query)

    if not normalized:
        return (
            "Civic Services Advisor can help with general information about "
            "government services, public offices, applications, documents, "
            "permits, certificates, and common civic procedures. "
            "Please provide the civic service you want to understand."
        )

    return (
        "Civic Services Advisor: "
        f"Your request concerns '{normalized}'. "
        "For accurate civic-service guidance, identify the specific service "
        "and the relevant country, county, city, or government authority. "
        "Requirements, fees, forms, office locations, processing times, and "
        "eligibility rules can vary by jurisdiction and may change over time. "
        "Use the official authority's current information before submitting "
        "documents, making payments, or relying on a deadline."
    )


def register_builtin_skills(registry: SkillRegistry) -> None:
    """
    Register all civic-services builtin skills into the supplied registry.
    """
    if not isinstance(registry, SkillRegistry):
        raise TypeError(
            "register_builtin_skills() requires a SkillRegistry."
        )

    registry.register(
        CIVIC_SERVICES_SKILL,
        _civic_services_handler,
    )


__all__ = [
    "CIVIC_SERVICES_SKILL",
    "register_builtin_skills",
]
