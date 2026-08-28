"""
NEXA Builtin Skill Tests: knowledge.remember_fact
"""

from skills.registry.registry import SkillRegistry
from skills.registry.authorization import SkillAuthorizationGate
from skills.builtin.knowledge_remember import (
    register_builtin_skills,
    REMEMBER_FACT_SKILL,
)


def test_skill_requires_knowledge_write_permission():
    registry = SkillRegistry()
    register_builtin_skills(registry)
    gate = SkillAuthorizationGate(registry)

    assert gate.is_authorized("knowledge.remember_fact", frozenset()) is False
    assert gate.is_authorized(
        "knowledge.remember_fact", frozenset({"KNOWLEDGE.WRITE"})
    ) is True


def test_skill_stores_fact_end_to_end():
    registry = SkillRegistry()
    register_builtin_skills(registry)
    gate = SkillAuthorizationGate(registry)

    handler = gate.get_authorized_handler(
        "knowledge.remember_fact", frozenset({"KNOWLEDGE.WRITE"})
    )
    result = handler(subject="nexa", predicate="is_a", value="operating system")

    assert result["status"] == "stored"
    assert result["subject"] == "nexa"


def test_manifest_shape():
    assert REMEMBER_FACT_SKILL.tier == "builtin"
    assert REMEMBER_FACT_SKILL.required_permissions == ("KNOWLEDGE.WRITE",)
