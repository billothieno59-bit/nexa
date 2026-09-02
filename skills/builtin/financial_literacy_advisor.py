"""
NEXA Africa Operating System
File: skills/builtin/financial_literacy_advisor.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Builtin skill providing general financial literacy reference
             information (savings approaches, mobile money safety
             basics, common terms) from a small curated table. This is
             general education, not financial advice or a
             recommendation to use any specific product — the response
             says so explicitly. Data is static and human-curated, not
             generated, since incorrect financial guidance can cause
             real harm to someone's savings and livelihood.
"""

from __future__ import annotations

from typing import Any, Dict

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry

FINANCIAL_LITERACY_SKILL = SkillManifest(
    skill_id="finance.literacy_advisor",
    name="Financial Literacy Advisor",
    description="Provides general financial literacy reference information on common topics.",
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)

# Static, curated reference data. General education only — not a
# recommendation for any specific product, provider, or course of
# action. Actual financial decisions depend on personal circumstances
# a static reference table cannot know.
_FINANCE_TOPICS: Dict[str, Dict[str, Any]] = {
    "savings": {
        "common_names": ["savings", "saving money", "how to save"],
        "summary": (
            "A common approach is paying into savings before spending on "
            "discretionary items, even a small fixed amount regularly, "
            "rather than saving only what happens to be left over."
        ),
        "common_tools": [
            "Bank savings accounts",
            "Mobile money savings/lock features",
            "Table banking / chama (rotating savings groups)",
        ],
        "notes": "Compare fees and withdrawal terms before choosing a tool.",
    },
    "mobile_money_safety": {
        "common_names": ["mobile money", "mpesa safety", "mobile money fraud"],
        "summary": (
            "Common safety practices: never share your PIN with anyone, "
            "including someone claiming to be from your provider; verify "
            "a recipient's registered name before sending money; be "
            "cautious of unsolicited messages asking you to reverse a "
            "transaction or claim a prize."
        ),
        "common_tools": ["Provider in-app fraud reporting", "Transaction PIN locks"],
        "notes": "Providers will not call asking for your PIN — that request is a common fraud pattern.",
    },
    "budgeting": {
        "common_names": ["budgeting", "budget", "managing money"],
        "summary": (
            "A common starting approach is listing fixed necessary "
            "expenses first, then discretionary spending, then savings — "
            "so it is clear what is actually available before spending."
        ),
        "common_tools": ["Notebook or paper ledger", "Basic budgeting apps", "Mobile money statements"],
        "notes": "Reviewing a full month before adjusting a budget avoids reacting to one unusual week.",
    },
    "credit_and_loans": {
        "common_names": ["credit", "loans", "borrowing money", "digital loans"],
        "summary": (
            "Before borrowing, it is common practice to check the total "
            "repayment amount (not just the monthly figure), the "
            "repayment period, and any penalty for late or early "
            "repayment."
        ),
        "common_tools": ["Bank loans", "Sacco loans", "Digital lending apps"],
        "notes": "Total cost of credit can vary significantly between lenders for the same amount borrowed.",
    },
}

_DISCLAIMER = (
    "This is general financial education only, not financial advice and "
    "not a recommendation of any specific product or provider. For "
    "decisions about your own finances, consider speaking with a "
    "qualified financial advisor or your bank/sacco directly."
)


def _financial_literacy_handler(topic: str) -> Dict[str, Any]:
    normalized = topic.strip().lower()

    for key, info in _FINANCE_TOPICS.items():
        if normalized == key or normalized in info["common_names"]:
            return {
                "status": "found",
                "topic": key,
                "guidance": {
                    "summary": info["summary"],
                    "common_tools": info["common_tools"],
                    "notes": info["notes"],
                },
                "disclaimer": _DISCLAIMER,
            }

    return {
        "status": "not_found",
        "topic": topic,
        "available_topics": list(_FINANCE_TOPICS.keys()),
        "disclaimer": _DISCLAIMER,
    }


def register_builtin_skills(registry: SkillRegistry) -> None:
    registry.register(FINANCIAL_LITERACY_SKILL, _financial_literacy_handler)


__all__ = [
    "FINANCIAL_LITERACY_SKILL",
    "register_builtin_skills",
]
