"""
NEXA Builtin Skill Tests: knowledge.recall_fact
"""

from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.builtin.knowledge_remember import register_builtin_skills as register_remember
from skills.builtin.knowledge_recall import register_builtin_skills as register_recall, RECALL_FACT_SKILL


def make_populated_registry():
    registry = SkillRegistry()
    register_remember(registry)
    register_recall(registry)
    gate = SkillAuthorizationGate(registry)

    remember = gate.get_authorized_handler(
        "knowledge.remember_fact", frozenset({"KNOWLEDGE.WRITE"})
    )
    remember(subject="nexa", predicate="is_a", value="operating system")

    return registry, gate


def test_skill_requires_knowledge_read_permission():
    registry = SkillRegistry()
    register_recall(registry)
    gate = SkillAuthorizationGate(registry)

    assert gate.is_authorized("knowledge.recall_fact", frozenset()) is False
    assert gate.is_authorized("knowledge.recall_fact", frozenset({"KNOWLEDGE.READ"})) is True


def test_recall_specific_predicate_found():
    registry, gate = make_populated_registry()
    handler = gate.get_authorized_handler("knowledge.recall_fact", frozenset({"KNOWLEDGE.READ"}))

    result = handler(subject="nexa", predicate="is_a")
    assert result["status"] == "found"
    assert result["value"] == "operating system"


def test_recall_specific_predicate_not_found():
    registry, gate = make_populated_registry()
    handler = gate.get_authorized_handler("knowledge.recall_fact", frozenset({"KNOWLEDGE.READ"}))

    result = handler(subject="nexa", predicate="nonexistent")
    assert result["status"] == "not_found"


def test_recall_all_facts_about_subject():
    registry, gate = make_populated_registry()
    handler = gate.get_authorized_handler("knowledge.recall_fact", frozenset({"KNOWLEDGE.READ"}))

    result = handler(subject="nexa")
    assert result["status"] == "found"
    assert len(result["facts"]) == 1


def test_manifest_shape():
    assert RECALL_FACT_SKILL.tier == "builtin"
    assert RECALL_FACT_SKILL.required_permissions == ("KNOWLEDGE.READ",)
