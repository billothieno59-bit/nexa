"""
NEXA NexaLocalProvider Tests. Fully offline, no external dependency.
"""

from core.knowledge.facts import Fact
from core.knowledge.store import FactStore
from core.cognition.providers.local_provider import NexaLocalProvider


def test_provider_name():
    provider = NexaLocalProvider(store=FactStore(db_path=":memory:"))
    assert provider.provider_name == "nexa_local"


def test_rejects_empty_prompt():
    provider = NexaLocalProvider(store=FactStore(db_path=":memory:"))
    result = provider.reason("   ")
    assert result["status"] == "rejected"


def test_returns_not_found_when_no_facts_stored():
    provider = NexaLocalProvider(store=FactStore(db_path=":memory:"))
    result = provider.reason("what is nexa")
    assert result["status"] == "not_found"


def test_finds_relevant_fact():
    store = FactStore(db_path=":memory:")
    store.add_fact(Fact(subject="nexa", predicate="is_a", value="operating system", provenance="user_stated"))

    provider = NexaLocalProvider(store=store)
    result = provider.reason("what is nexa")

    assert result["status"] == "ok"
    assert "operating system" in result["response"]
    assert result["provider"] == "nexa_local"
