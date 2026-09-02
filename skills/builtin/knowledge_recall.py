"""
NEXA Africa Operating System
File: skills/builtin/knowledge_recall.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Builtin skill that reads facts back from FactStore.
             Symmetric counterpart to knowledge.remember_fact — completes
             the write/read cycle for durable knowledge.

             Also exposes FactStore.get_related() (a cycle-safe breadth-
             first walk over stored facts) via an optional max_depth
             parameter, so relationship queries go through the same
             governed, authorized skill as flat fact lookups rather than
             a separate unauthorized API endpoint.

             register_builtin_skills() accepts an optional store
             parameter so tests can inject an isolated FactStore
             (e.g. FactStore(db_path=":memory:")) instead of sharing
             the default persistent data/knowledge_facts.db across
             every test in the suite. Production callers that omit
             store keep the exact previous behavior — a single shared
             default store, lazily created once.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry
from core.knowledge.store import FactStore

RECALL_FACT_SKILL = SkillManifest(
    skill_id="knowledge.recall_fact",
    name="Recall Fact",
    description=(
        "Retrieves a stored fact by subject and predicate, all facts "
        "about a subject, or related facts up to a given depth."
    ),
    tier="builtin",
    required_permissions=("KNOWLEDGE.READ",),
)

_default_store: Optional[FactStore] = None


def _get_default_store() -> FactStore:
    global _default_store
    if _default_store is None:
        _default_store = FactStore()
    return _default_store


def register_builtin_skills(registry: SkillRegistry, store: Optional[FactStore] = None) -> None:
    active_store = store or _get_default_store()

    def _recall_fact_handler(
        subject: str,
        predicate: Optional[str] = None,
        max_depth: Optional[int] = None,
    ) -> Dict[str, Any]:
        if max_depth is not None:
            if not isinstance(max_depth, int) or max_depth < 0:
                return {
                    "status": "rejected",
                    "error": "max_depth must be a non-negative integer.",
                }

            related_facts = active_store.get_related(subject, max_depth=max_depth)
            return {
                "status": "found" if related_facts else "not_found",
                "subject": subject,
                "max_depth": max_depth,
                "related_facts": [
                    {
                        "subject": f.subject,
                        "predicate": f.predicate,
                        "value": f.value,
                        "provenance": f.provenance,
                    }
                    for f in related_facts
                ],
            }

        if predicate is not None:
            fact = active_store.get_fact(subject, predicate)
            if fact is None:
                return {"status": "not_found", "subject": subject, "predicate": predicate}
            return {
                "status": "found",
                "subject": fact.subject,
                "predicate": fact.predicate,
                "value": fact.value,
                "provenance": fact.provenance,
            }

        facts = active_store.get_facts_about(subject)
        return {
            "status": "found" if facts else "not_found",
            "subject": subject,
            "facts": [{"predicate": f.predicate, "value": f.value, "provenance": f.provenance} for f in facts],
        }

    registry.register(RECALL_FACT_SKILL, _recall_fact_handler)


__all__ = [
    "RECALL_FACT_SKILL",
    "register_builtin_skills",
]
