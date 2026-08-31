"""
NEXA Builtin Skill Tests: knowledge.remember_fact
"""

from core.knowledge.store import FactStore
from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.builtin.knowledge_remember import (
    register_builtin_skills,
    REMEMBER_FACT_SKILL,
)


def test_skill_requires_knowledge_write_permission():
    store = FactStore(db_path=":memory:")
    registry = SkillRegistry()
    register_builtin_skills(registry, store=store)
    gate = SkillAuthorizationGate(registry)

    assert gate.is_authorized("knowledge.remember_fact", frozenset()) is False
    assert gate.is_authorized(
        "knowledge.remember_fact", frozenset({"KNOWLEDGE.WRITE"})
    ) is True


def test_skill_stores_fact_end_to_end():
    store = FactStore(db_path=":memory:")
    registry = SkillRegistry()
    register_builtin_skills(registry, store=store)
    gate = SkillAuthorizationGate(registry)

    handler = gate.get_authorized_handler(
        "knowledge.remember_fact", frozenset({"KNOWLEDGE.WRITE"})
    )
    result = handler(subject="nexa", predicate="is_a", value="operating system")

    assert result["status"] == "stored"
    assert result["subject"] == "nexa"

    # Prove it actually persisted in the injected store, not just
    # returned a success-shaped dict.
    stored = store.get_fact("nexa", "is_a")
    assert stored is not None
    assert stored.value == "operating system"


def test_default_store_is_used_when_none_injected():
    """
    Confirms omitting store still works exactly as before — production
    callers are unaffected by this change.
    """
    registry = SkillRegistry()
    register_builtin_skills(registry)
    gate = SkillAuthorizationGate(registry)

    handler = gate.get_authorized_handler(
        "knowledge.remember_fact", frozenset({"KNOWLEDGE.WRITE"})
    )
    result = handler(subject="default_store_smoke_test", predicate="works", value="yes")
    assert result["status"] == "stored"


def test_manifest_shape():
    assert REMEMBER_FACT_SKILL.tier == "builtin"
    assert REMEMBER_FACT_SKILL.required_permissions == ("KNOWLEDGE.WRITE",)
