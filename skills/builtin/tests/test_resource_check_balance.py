"""
NEXA Builtin Skill Tests: resource.check_balance
"""

from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.builtin.resource_check_balance import (
    register_builtin_skills as register_check_balance,
    CHECK_BALANCE_SKILL,
)


def make_registry():
    registry = SkillRegistry()
    register_check_balance(registry)
    gate = SkillAuthorizationGate(registry)
    return registry, gate


def test_skill_requires_resource_read_permission():
    registry, gate = make_registry()
    assert gate.is_authorized("resource.check_balance", frozenset()) is False
    assert gate.is_authorized("resource.check_balance", frozenset({"RESOURCE.READ"})) is True


def test_balance_for_unknown_subject_is_zero():
    registry, gate = make_registry()
    handler = gate.get_authorized_handler("resource.check_balance", frozenset({"RESOURCE.READ"}))
    result = handler(subject="a_subject_with_no_transactions_zzz", resource="credits")
    assert result["status"] == "found"
    assert result["balance"] == 0.0


def test_rejects_empty_subject():
    registry, gate = make_registry()
    handler = gate.get_authorized_handler("resource.check_balance", frozenset({"RESOURCE.READ"}))
    result = handler(subject="", resource="credits")
    assert result["status"] == "rejected"


def test_rejects_empty_resource():
    registry, gate = make_registry()
    handler = gate.get_authorized_handler("resource.check_balance", frozenset({"RESOURCE.READ"}))
    result = handler(subject="bill", resource="")
    assert result["status"] == "rejected"


def test_manifest_shape():
    assert CHECK_BALANCE_SKILL.tier == "builtin"
    assert CHECK_BALANCE_SKILL.required_permissions == ("RESOURCE.READ",)


def test_reads_balance_written_by_resource_transaction_handler():
    from core.execution.executor.action_handlers import ResourceTransactionHandler
    from core.execution.orchestrator.planner.planner import PlanStep
    from core.knowledge.store import FactStore
    import skills.builtin.resource_check_balance as check_balance_module

    shared_store = FactStore(db_path=":memory:")
    check_balance_module._store = shared_store

    tx_handler = ResourceTransactionHandler(store=shared_store)
    tx_handler.handle(
        PlanStep(
            action="INTENT_RESOURCE_VALUE_TRANSACT",
            parameters={"subject": "bill", "resource": "credits", "delta": 25},
        )
    )

    registry, gate = make_registry()
    handler = gate.get_authorized_handler("resource.check_balance", frozenset({"RESOURCE.READ"}))
    result = handler(subject="bill", resource="credits")
    assert result["status"] == "found"
    assert result["balance"] == 25.0
