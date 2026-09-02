"""
NEXA Africa Operating System
File: skills/builtin/tenancy_rights_advisor.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Builtin skill providing general tenant/landlord reference
             information (deposits, notice periods, common terms) from
             a small curated table. This is general reference
             information, not legal advice specific to any lease or
             jurisdiction — the response says so explicitly. Data is
             static and human-curated, not generated, since incorrect
             legal-adjacent guidance can cause real harm to someone's
             housing situation.
"""

from __future__ import annotations

from typing import Any, Dict

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry

TENANCY_RIGHTS_SKILL = SkillManifest(
    skill_id="housing.tenancy_rights_advisor",
    name="Tenancy Rights Advisor",
    description="Provides general tenant/landlord reference information on common topics.",
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)

# Static, curated reference data. General information only — actual
# tenant/landlord rights depend on the specific lease terms and the
# jurisdiction's actual tenancy law, which a static reference table
# cannot know or substitute for.
_TENANCY_TOPICS: Dict[str, Dict[str, Any]] = {
    "security_deposit": {
        "common_names": ["deposit", "security deposit", "rent deposit"],
        "summary": (
            "A security deposit is commonly held to cover damage beyond "
            "normal wear and tear, or unpaid rent — not as an automatic "
            "forfeit if the tenancy simply ends. It is common practice "
            "to document the unit's condition (photos, a signed "
            "checklist) at move-in, so its state at move-out can be "
            "compared fairly."
        ),
        "notes": (
            "Keep a copy of the lease and any move-in condition report; "
            "ask for a written receipt for the deposit."
        ),
    },
    "notice_period": {
        "common_names": ["notice period", "moving out notice", "eviction notice"],
        "summary": (
            "Lease agreements commonly specify a minimum notice period "
            "before either party ends a tenancy. This period, and "
            "whether it differs for the tenant versus the landlord, is "
            "usually stated explicitly in the signed lease."
        ),
        "notes": "Check the specific lease document first; notice requirements can also be set by local tenancy law.",
    },
    "rent_increases": {
        "common_names": ["rent increase", "raising rent"],
        "summary": (
            "It is common for leases to specify whether and how rent "
            "can be increased during a fixed term, and what notice is "
            "required before an increase takes effect at renewal."
        ),
        "notes": (
            "A fixed-term lease's agreed rent is often protected from "
            "change until that term ends, per its own wording."
        ),
    },
    "repairs_and_maintenance": {
        "common_names": ["repairs", "maintenance", "who pays for repairs"],
        "summary": (
            "Responsibility for repairs is commonly split by cause: "
            "structural or pre-existing issues are often the landlord's "
            "responsibility, while damage caused by the tenant is often "
            "theirs — but the exact split is normally defined in the "
            "lease itself."
        ),
        "notes": (
            "Reporting repair needs in writing (even a text message) "
            "creates a record of when the issue was raised."
        ),
    },
}

_DISCLAIMER = (
    "This is general reference information only, not legal advice "
    "specific to your lease or your local tenancy law. For a situation "
    "involving a real dispute or a specific lease, consider consulting "
    "a qualified lawyer or your local tenancy/housing authority."
)


def _tenancy_rights_handler(topic: str) -> Dict[str, Any]:
    normalized = topic.strip().lower()

    for key, info in _TENANCY_TOPICS.items():
        if normalized == key or normalized in info["common_names"]:
            return {
                "status": "found",
                "topic": key,
                "guidance": {
                    "summary": info["summary"],
                    "notes": info["notes"],
                },
                "disclaimer": _DISCLAIMER,
            }

    return {
        "status": "not_found",
        "topic": topic,
        "available_topics": list(_TENANCY_TOPICS.keys()),
        "disclaimer": _DISCLAIMER,
    }


def register_builtin_skills(registry: SkillRegistry) -> None:
    registry.register(TENANCY_RIGHTS_SKILL, _tenancy_rights_handler)


__all__ = [
    "TENANCY_RIGHTS_SKILL",
    "register_builtin_skills",
]
