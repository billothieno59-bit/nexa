"""
NEXA Africa Operating System
File: skills/builtin/resource_check_balance.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Builtin skill that reads a resource balance back from
             FactStore. Read-only counterpart to
             core/execution/executor/action_handlers.py's
             ResourceTransactionHandler — completes the write/read
             cycle for resource balances the same way
             knowledge.recall_fact completes it for general facts.

             Note: RESOURCE_PREDICATE_PREFIX below is intentionally
             duplicated from action_handlers.py rather than imported,
             to avoid a circular import (action_handlers.py imports
             skills.registry.bootstrap, which registers this skill
             module). Must be kept identical to
             core/execution/executor/action_handlers.py's
             RESOURCE_PREDICATE_PREFIX — currently "resource_balance:".
"""

from __future__ import annotations

from typing import Any, Dict

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry
from core.knowledge.store import FactStore

RESOURCE_PREDICATE_PREFIX = "resource_balance:"

CHECK_BALANCE_SKILL = SkillManifest(
    skill_id="resource.check_balance",
    name="Check Resource Balance",
    description=(
        "Reads a subject's current balance for a named resource, "
        "as maintained by resource transactions. Returns 0 if no "
        "transaction has ever been recorded for that subject/resource."
    ),
    tier="builtin",
    required_permissions=("RESOURCE.READ",),
)

_store = FactStore()


def _check_balance_handler(subject: str, resource: str) -> Dict[str, Any]:
    if not isinstance(subject, str) or not subject.strip():
        return {"status": "rejected", "error": "subject must be a non-empty string."}

    if not isinstance(resource, str) or not resource.strip():
        return {"status": "rejected", "error": "resource must be a non-empty string."}

    fact = _store.get_fact(subject, f"{RESOURCE_PREDICATE_PREFIX}{resource}")

    if fact is None:
        return {"status": "found", "subject": subject, "resource": resource, "balance": 0.0}

    try:
        balance = float(fact.value)
    except (TypeError, ValueError):
        return {
            "status": "error",
            "error": "Stored balance was not numeric.",
            "subject": subject,
            "resource": resource,
        }

    return {"status": "found", "subject": subject, "resource": resource, "balance": balance}


def register_builtin_skills(registry: SkillRegistry) -> None:
    registry.register(CHECK_BALANCE_SKILL, _check_balance_handler)


__all__ = [
    "CHECK_BALANCE_SKILL",
    "register_builtin_skills",
]
