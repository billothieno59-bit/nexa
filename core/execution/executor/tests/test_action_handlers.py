"""
NEXA Execution Action Handlers Tests.
"""

from core.execution.executor.bootstrap import get_handler_registry
from core.execution.executor.action_handlers import (
    DiagnosticCheckHandler,
    ResourceTransactionHandler,
)
from core.execution.orchestrator.planner.planner import PlanStep
from core.knowledge.store import FactStore


def test_diagnostic_handler_is_registered():
    registry = get_handler_registry()
    assert registry.has_handler("INTENT_SYSTEM_DIAGNOSTIC_CHECK")


def test_resource_transaction_handler_is_registered():
    registry = get_handler_registry()
    assert registry.has_handler("INTENT_RESOURCE_VALUE_TRANSACT")


def test_diagnostic_handler_resolves_to_correct_type():
    registry = get_handler_registry()
    handler = registry.get_handler("INTENT_SYSTEM_DIAGNOSTIC_CHECK")
    assert isinstance(handler, DiagnosticCheckHandler)


def test_resource_transaction_handler_resolves_to_correct_type():
    registry = get_handler_registry()
    handler = registry.get_handler("INTENT_RESOURCE_VALUE_TRANSACT")
    assert isinstance(handler, ResourceTransactionHandler)


def test_unregistered_action_is_not_found():
    registry = get_handler_registry()
    assert not registry.has_handler("INTENT_UNKNOWN_OR_MALICIOUS")


def test_resource_transaction_credits_a_new_subject():
    handler = ResourceTransactionHandler(store=FactStore(db_path=":memory:"))
    step = PlanStep(
        action="INTENT_RESOURCE_VALUE_TRANSACT",
        parameters={"subject": "bill", "resource": "credits", "delta": 10},
    )
    result = handler.handle(step)
    assert result["status"] == "ok"
    assert result["previous_balance"] == 0.0
    assert result["new_balance"] == 10.0


def test_resource_transaction_accumulates_across_calls():
    store = FactStore(db_path=":memory:")
    handler = ResourceTransactionHandler(store=store)
    handler.handle(
        PlanStep(
            action="INTENT_RESOURCE_VALUE_TRANSACT",
            parameters={"subject": "bill", "resource": "credits", "delta": 10},
        )
    )
    result = handler.handle(
        PlanStep(
            action="INTENT_RESOURCE_VALUE_TRANSACT",
            parameters={"subject": "bill", "resource": "credits", "delta": -3},
        )
    )
    assert result["status"] == "ok"
    assert result["previous_balance"] == 10.0
    assert result["new_balance"] == 7.0


def test_resource_transaction_rejects_insufficient_balance():
    handler = ResourceTransactionHandler(store=FactStore(db_path=":memory:"))
    step = PlanStep(
        action="INTENT_RESOURCE_VALUE_TRANSACT",
        parameters={"subject": "bill", "resource": "credits", "delta": -5},
    )
    result = handler.handle(step)
    assert result["status"] == "rejected"
    assert result["error"] == "insufficient_balance"


def test_resource_transaction_rejects_missing_subject():
    handler = ResourceTransactionHandler(store=FactStore(db_path=":memory:"))
    step = PlanStep(
        action="INTENT_RESOURCE_VALUE_TRANSACT",
        parameters={"resource": "credits", "delta": 5},
    )
    result = handler.handle(step)
    assert result["status"] == "rejected"


def test_resource_transaction_rejects_non_numeric_delta():
    handler = ResourceTransactionHandler(store=FactStore(db_path=":memory:"))
    step = PlanStep(
        action="INTENT_RESOURCE_VALUE_TRANSACT",
        parameters={"subject": "bill", "resource": "credits", "delta": "ten"},
    )
    result = handler.handle(step)
    assert result["status"] == "rejected"


def test_resource_transaction_keeps_separate_balances_per_resource():
    store = FactStore(db_path=":memory:")
    handler = ResourceTransactionHandler(store=store)
    handler.handle(
        PlanStep(
            action="INTENT_RESOURCE_VALUE_TRANSACT",
            parameters={"subject": "bill", "resource": "credits", "delta": 10},
        )
    )
    result = handler.handle(
        PlanStep(
            action="INTENT_RESOURCE_VALUE_TRANSACT",
            parameters={"subject": "bill", "resource": "api_quota", "delta": 3},
        )
    )
    assert result["new_balance"] == 3.0
