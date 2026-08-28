"""
NEXA Africa Operating System
File: skills/builtin/knowledge_recall.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Builtin skill that reads facts back from FactStore.
             Symmetric counterpart to knowledge.remember_fact — completes
             the write/read cycle for durable knowledge.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry
from core.knowledge.store import FactStore

RECALL_FACT_SKILL = SkillManifest(
    skill_id="knowledge.recall_fact",
    name="Recall Fact",
    description="Retrieves a stored fact by subject and predicate, or all facts about a subject.",
    tier="builtin",
    required_permissions=("KNOWLEDGE.READ",),
)

_store = FactStore()


def _recall_fact_handler(subject: str, predicate: Optional[str] = None) -> Dict[str, Any]:
    if predicate is not None:
        fact = _store.get_fact(subject, predicate)
        if fact is None:
            return {"status": "not_found", "subject": subject, "predicate": predicate}
        return {
            "status": "found",
            "subject": fact.subject,
            "predicate": fact.predicate,
            "value": fact.value,
            "provenance": fact.provenance,
        }

    facts = _store.get_facts_about(subject)
    return {
        "status": "found" if facts else "not_found",
        "subject": subject,
        "facts": [
            {"predicate": f.predicate, "value": f.value, "provenance": f.provenance}
            for f in facts
        ],
    }


def register_builtin_skills(registry: SkillRegistry) -> None:
    registry.register(RECALL_FACT_SKILL, _recall_fact_handler)


__all__ = [
    "RECALL_FACT_SKILL",
    "register_builtin_skills",
]
