"""
NEXA Africa Operating System
File: core/execution/executor/action_handlers.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Concrete action handlers registered with the canonical
             HandlerRegistry. DiagnosticCheckHandler reports real
             system state. ResourceTransactionHandler now has a real,
             explicitly-assumed implementation (see its docstring for
             the assumption made in the absence of a formal product
             spec) rather than being a no-op.
"""

from __future__ import annotations

from typing import Optional

from core.execution.executor.handler import ExecutionActionHandler
from core.execution.orchestrator.planner.planner import PlanStep
from core.knowledge.facts import Fact
from core.knowledge.store import FactStore
from core.services.logging.logger import get_logger
from skills.registry.bootstrap import global_skill_registry

logger = get_logger(__name__)

RESOURCE_PREDICATE_PREFIX = "resource_balance:"


class DiagnosticCheckHandler(ExecutionActionHandler):
    """
    Reports real diagnostic state: number of registered skills and
    their ids. No external side effects.
    """

    @property
    def action_name(self) -> str:
        return "INTENT_SYSTEM_DIAGNOSTIC_CHECK"

    def handle(self, step: PlanStep) -> dict:
        skill_ids = global_skill_registry.list_skill_ids()
        return {
            "status": "ok",
            "registered_skills_count": len(skill_ids),
            "registered_skill_ids": list(skill_ids),
        }


class ResourceTransactionHandler(ExecutionActionHandler):
    """
    Applies a signed balance change to a named resource for a subject.

    ASSUMPTION MADE HERE, NOT A CONFIRMED PRODUCT SPEC: no formal
    definition of "resource transaction" existed when this was
    written. In its absence, this handler treats it as the simplest
    generic case a "resource" word plausibly means across likely uses
    (API call credits, skill-usage quotas, or similar countable
    allowances): a named, per-subject running balance that a
    transaction adjusts by a signed delta. This reuses the existing
    FactStore (core/knowledge/store.py) rather than introducing a new
    table — a balance is stored as a fact with predicate
    "resource_balance:<resource_name>", value the current balance as a
    string, superseded on every transaction exactly like any other
    fact. If this does not match the intended product meaning, only
    this class needs to change — no caller depends on its internals.

    Fails closed: rejects malformed parameters, and rejects (does not
    apply) a transaction that would take a balance below zero, since
    silently allowing negative balances is a stronger, unstated
    assumption than declining the transaction.
    """

    def __init__(self, store: Optional[FactStore] = None) -> None:
        self._store = store or FactStore()

    @property
    def action_name(self) -> str:
        return "INTENT_RESOURCE_VALUE_TRANSACT"

    def _get_balance(self, subject: str, resource: str) -> float:
        fact = self._store.get_fact(subject, f"{RESOURCE_PREDICATE_PREFIX}{resource}")
        if fact is None:
            return 0.0
        try:
            return float(fact.value)
        except (TypeError, ValueError):
            logger.warning(
                "Stored resource balance for subject=%s resource=%s was not numeric; treating as 0.",
                subject,
                resource,
            )
            return 0.0

    def handle(self, step: PlanStep) -> dict:
        params = step.parameters or {}
        subject = params.get("subject")
        resource = params.get("resource")
        delta = params.get("delta")

        if not isinstance(subject, str) or not subject.strip():
            return {"status": "rejected", "error": "parameters.subject must be a non-empty string."}

        if not isinstance(resource, str) or not resource.strip():
            return {"status": "rejected", "error": "parameters.resource must be a non-empty string."}

        if not isinstance(delta, (int, float)) or isinstance(delta, bool):
            return {"status": "rejected", "error": "parameters.delta must be a number."}

        current_balance = self._get_balance(subject, resource)
        new_balance = current_balance + delta

        if new_balance < 0:
            return {
                "status": "rejected",
                "error": "insufficient_balance",
                "subject": subject,
                "resource": resource,
                "current_balance": current_balance,
                "requested_delta": delta,
            }

        self._store.add_fact(
            Fact(
                subject=subject,
                predicate=f"{RESOURCE_PREDICATE_PREFIX}{resource}",
                value=str(new_balance),
                provenance="resource_transaction",
            )
        )

        logger.info(
            "Resource transaction applied subject=%s resource=%s delta=%s new_balance=%s",
            subject,
            resource,
            delta,
            new_balance,
        )

        return {
            "status": "ok",
            "subject": subject,
            "resource": resource,
            "previous_balance": current_balance,
            "delta": delta,
            "new_balance": new_balance,
        }


__all__ = [
    "DiagnosticCheckHandler",
    "ResourceTransactionHandler",
]
