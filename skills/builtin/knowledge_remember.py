"""
NEXA Africa Operating System
File: skills/builtin/knowledge_remember.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Builtin skill that writes a durable Fact to FactStore.
             This is the first real path from skill execution into
             core/knowledge/ — previously FactStore had no way to be
             written to except by calling it directly in tests.
"""

from __future__ import annotations

from typing import Any, Dict

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry
from core.knowledge.facts import Fact
from core.knowledge.store import FactStore

REMEMBER_FACT_SKILL = SkillManifest(
    skill_id="knowledge.remember_fact",
    name="Remember Fact",
    description="Stores a durable subject/predicate/value fact in knowledge storage.",
    tier="builtin",
    required_permissions=("KNOWLEDGE.WRITE",),
)

_store = FactStore()


def _remember_fact_handler(
    subject: str,
    predicate: str,
    value: str,
    provenance: str = "skill_invocation",
) -> Dict[str, Any]:
    fact = Fact(subject=subject, predicate=predicate, value=value, provenance=provenance)
    _store.add_fact(fact)
    return {
        "status": "stored",
        "subject": subject,
        "predicate": predicate,
        "value": value,
    }


def register_builtin_skills(registry: SkillRegistry) -> None:
    registry.register(REMEMBER_FACT_SKILL, _remember_fact_handler)


__all__ = [
    "REMEMBER_FACT_SKILL",
    "register_builtin_skills",
]
