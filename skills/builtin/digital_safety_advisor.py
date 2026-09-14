"""
NEXA Africa Operating System
File: skills/builtin/digital_safety_advisor.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Builtin skill providing general online safety reference
             information (phishing, passwords, account recovery,
             public wifi) from a small curated table. This is general
             awareness only, not a substitute for your specific
             provider's official security guidance — the response
             says so explicitly. Data is static and human-curated,
             not generated, since incorrect security guidance can
             leave someone more exposed, not less.
"""

from __future__ import annotations

from typing import Any, Dict

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry

DIGITAL_SAFETY_SKILL = SkillManifest(
    skill_id="digital.online_safety_advisor",
    name="Online Safety Advisor",
    description="Provides general online safety reference information on common topics.",
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)

_SAFETY_TOPICS: Dict[str, Dict[str, Any]] = {
    "phishing": {
        "common_names": ["phishing", "scam messages", "fake links"],
        "summary": (
            "Phishing attempts commonly create urgency (\"act now or lose "
            "access\") and ask you to click a link or share a code/password. "
            "Legitimate providers rarely ask for your password or a one-time "
            "code through a message you did not request."
        ),
        "notes": "When unsure, go directly to the provider's official app or website instead of clicking a link in a message.",
    },
    "strong_passwords": {
        "common_names": ["passwords", "strong password", "password safety"],
        "summary": (
            "A longer, unique passphrase for each important account is "
            "generally stronger than a short complex password reused "
            "across multiple accounts — reuse means one leak exposes "
            "everything."
        ),
        "notes": "A password manager can generate and store unique passwords per account so you don't have to memorize them all.",
    },
    "account_recovery": {
        "common_names": ["account recovery", "locked out", "recovery options"],
        "summary": (
            "Setting up recovery options (a backup email, phone number, or "
            "recovery codes) before you need them is what makes regaining "
            "access possible if you're ever locked out."
        ),
        "notes": "Recovery codes are commonly meant to be saved somewhere offline, not just left in an easily-searched inbox.",
    },
    "public_wifi_safety": {
        "common_names": ["public wifi", "wifi safety", "open network"],
        "summary": (
            "On an open public wifi network, avoid logging into sensitive "
            "accounts (banking, mobile money) unless the connection uses "
            "HTTPS, since traffic on an open network can potentially be "
            "observed by others on the same network."
        ),
        "notes": "A site address starting with \"https://\" (not just \"http://\") indicates an encrypted connection.",
    },
}

_DISCLAIMER = (
    "This is general online safety awareness only, not a substitute for "
    "your specific bank, mobile money provider, or platform's official "
    "security guidance. If you suspect your account has been "
    "compromised, contact that provider directly through their official "
    "channels."
)


def _digital_safety_handler(topic: str) -> Dict[str, Any]:
    normalized = topic.strip().lower()

    for key, info in _SAFETY_TOPICS.items():
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
        "available_topics": list(_SAFETY_TOPICS.keys()),
        "disclaimer": _DISCLAIMER,
    }


def register_builtin_skills(registry: SkillRegistry) -> None:
    registry.register(DIGITAL_SAFETY_SKILL, _digital_safety_handler)


__all__ = [
    "DIGITAL_SAFETY_SKILL",
    "register_builtin_skills",
]
