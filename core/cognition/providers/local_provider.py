"""
NEXA Africa Operating System
File: core/cognition/providers/local_provider.py
Constitutional Owner: Bill Odhiambo Othieno
Description: NexaLocalProvider — the first real seed of NEXA's own,
             independent reasoning capability. Fully offline, no
             external API, no cost. Honest about scope: it answers by
             finding the most relevant fact NEXA has actually stored via
             FactStore (word-overlap matching), not by general reasoning.
             It gets more useful as core/knowledge/ accumulates real
             facts through skills like knowledge.remember_fact. This is
             deliberately narrow — a real, working starting point for
             "NEXA's own AI," not a general-purpose reasoner.
"""

from __future__ import annotations

from typing import Any, Dict, List

from core.cognition.providers.base import ReasoningProvider
from core.knowledge.store import FactStore
from core.services.logging.logger import get_logger

logger = get_logger(__name__)


class NexaLocalProvider(ReasoningProvider):
    """
    Answers a prompt by finding the stored fact whose subject/predicate
    words overlap most with the prompt's words. Fully local, fully
    offline. Returns "not_found" rather than fabricating an answer when
    nothing relevant is stored.
    """

    def __init__(self, store: FactStore | None = None) -> None:
        self._store = store or FactStore()

    @property
    def provider_name(self) -> str:
        return "nexa_local"

    def _score_overlap(self, prompt_words: set, fact_subject: str, fact_predicate: str) -> int:
        fact_words = set(fact_subject.lower().split()) | set(fact_predicate.lower().split())
        return len(prompt_words & fact_words)

    def reason(self, prompt: str, max_tokens: int = 1024) -> Dict[str, Any]:
        if not isinstance(prompt, str) or not prompt.strip():
            return {"status": "rejected", "error": "prompt must be a non-empty string."}

        prompt_words = set(prompt.lower().split())

        # Search stored facts for the best word-overlap match. This is
        # intentionally simple — a real starting point, not a fabricated
        # capability. It will only find what NEXA has actually been told.
        candidates: List[Dict[str, Any]] = []
        for word in prompt_words:
            for fact in self._store.get_facts_about(word):
                candidates.append(fact)

        if not candidates:
            return {
                "status": "not_found",
                "provider": self.provider_name,
                "message": "NEXA's local knowledge has nothing relevant stored yet.",
            }

        best = max(
            candidates,
            key=lambda f: self._score_overlap(prompt_words, f.subject, f.predicate),
        )

        return {
            "status": "ok",
            "response": f"{best.subject} {best.predicate}: {best.value}",
            "provider": self.provider_name,
            "source_fact": {"subject": best.subject, "predicate": best.predicate, "value": best.value},
        }


__all__ = [
    "NexaLocalProvider",
]
