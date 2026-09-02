"""
NEXA Builtin Skill Tests: knowledge.recall_fact
"""

from core.knowledge.store import FactStore
from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.builtin.knowledge_remember import register_builtin_skills as register_remember
from skills.builtin.knowledge_recall import register_builtin_skills as register_recall, RECALL_FACT_SKILL


def make_populated_registry():
    store = FactStore(db_path=":memory:")
    registry = SkillRegistry()
    register_remember(registry, store=store)
    register_recall(registry, store=store)
    gate = SkillAuthorizationGate(registry)
    remember = gate.get_authorized_handler("knowledge.remember_fact", frozenset({"KNOWLEDGE.WRITE"}))
    remember(subject="nexa", predicate="is_a", value="operating system")
    return registry, gate


def make_related_registry():
    store = FactStore(db_path=":memory:")
    registry = SkillRegistry()
    register_remember(registry, store=store)
    register_recall(registry, store=store)
    gate = SkillAuthorizationGate(registry)
    remember = gate.get_authorized_handler("knowledge.remember_fact", frozenset({"KNOWLEDGE.WRITE"}))
    remember(subject="farmer_a", predicate="member_of", value="cooperative_x")
    remember(subject="cooperative_x", predicate="based_in", value="Nairobi")
    return registry, gate


def test_skill_requires_knowledge_read_permission():
    store = FactStore(db_path=":memory:")
    registry = SkillRegistry()
    register_recall(registry, store=store)
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


def test_recall_related_facts_single_hop():
    registry, gate = make_related_registry()
    handler = gate.get_authorized_handler("knowledge.recall_fact", frozenset({"KNOWLEDGE.READ"}))
    result = handler(subject="farmer_a", max_depth=1)
    assert result["status"] == "found"
    assert result["max_depth"] == 1
    assert len(result["related_facts"]) == 1
    assert result["related_facts"][0]["value"] == "cooperative_x"


def test_recall_related_facts_two_hops():
    registry, gate = make_related_registry()
    handler = gate.get_authorized_handler("knowledge.recall_fact", frozenset({"KNOWLEDGE.READ"}))
    result = handler(subject="farmer_a", max_depth=2)
    assert result["status"] == "found"
    values = {f["value"] for f in result["related_facts"]}
    assert values == {"cooperative_x", "Nairobi"}


def test_recall_related_facts_no_relations_returns_not_found():
    # "nexa" itself has a fact (is_a: operating system), so it's not
    # a valid "zero relations" case — get_related() correctly reports
    # that edge as a related fact. Use a subject with genuinely no
    # facts at all in this isolated store instead.
    registry, gate = make_populated_registry()
    handler = gate.get_authorized_handler("knowledge.recall_fact", frozenset({"KNOWLEDGE.READ"}))
    result = handler(subject="subject_with_no_facts_at_all", max_depth=3)
    assert result["status"] == "not_found"
    assert result["related_facts"] == []


def test_recall_rejects_negative_max_depth():
    registry, gate = make_populated_registry()
    handler = gate.get_authorized_handler("knowledge.recall_fact", frozenset({"KNOWLEDGE.READ"}))
    result = handler(subject="nexa", max_depth=-1)
    assert result["status"] == "rejected"


def test_manifest_shape():
    assert RECALL_FACT_SKILL.tier == "builtin"
    assert RECALL_FACT_SKILL.required_permissions == ("KNOWLEDGE.READ",)
