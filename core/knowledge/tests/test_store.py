"""
NEXA FactStore Tests.
"""

from core.knowledge.facts import Fact
from core.knowledge.store import FactStore


def test_add_and_retrieve_fact(tmp_path):
    db_file = tmp_path / "test_facts.db"
    store = FactStore(db_path=str(db_file))

    fact = Fact(subject="nexa", predicate="is_a", value="operating system", provenance="user_stated")
    assert store.add_fact(fact) is True

    results = store.get_facts_about("nexa")
    assert len(results) == 1
    assert results[0].value == "operating system"


def test_get_facts_about_unknown_subject_returns_empty(tmp_path):
    db_file = tmp_path / "test_facts.db"
    store = FactStore(db_path=str(db_file))
    assert store.get_facts_about("nonexistent") == []


def test_add_fact_rejects_non_fact(tmp_path):
    db_file = tmp_path / "test_facts.db"
    store = FactStore(db_path=str(db_file))
    try:
        store.add_fact("not a fact")
        assert False, "expected TypeError"
    except TypeError:
        pass


def test_adding_fact_with_same_subject_predicate_supersedes_old_value(tmp_path):
    db_file = tmp_path / "test_facts.db"
    store = FactStore(db_path=str(db_file))

    old_fact = Fact(subject="user", predicate="favorite_language", value="Python", provenance="user_stated")
    store.add_fact(old_fact)

    new_fact = Fact(subject="user", predicate="favorite_language", value="Swahili", provenance="user_stated")
    store.add_fact(new_fact)

    results = store.get_facts_about("user")
    assert len(results) == 1
    assert results[0].value == "Swahili"


def test_get_fact_returns_specific_predicate(tmp_path):
    db_file = tmp_path / "test_facts.db"
    store = FactStore(db_path=str(db_file))

    store.add_fact(Fact(subject="nexa", predicate="is_a", value="operating system", provenance="user_stated"))
    store.add_fact(Fact(subject="nexa", predicate="creator", value="Bill Odhiambo Othieno", provenance="user_stated"))

    result = store.get_fact("nexa", "is_a")
    assert result is not None
    assert result.value == "operating system"


def test_get_fact_returns_none_when_not_found(tmp_path):
    db_file = tmp_path / "test_facts.db"
    store = FactStore(db_path=str(db_file))
    assert store.get_fact("nexa", "nonexistent_predicate") is None


def test_get_facts_by_predicate_returns_all_matching_subjects(tmp_path):
    db_file = tmp_path / "test_facts.db"
    store = FactStore(db_path=str(db_file))

    store.add_fact(Fact(subject="farmer_a", predicate="grows", value="maize", provenance="user_stated"))
    store.add_fact(Fact(subject="farmer_b", predicate="grows", value="beans", provenance="user_stated"))
    store.add_fact(Fact(subject="farmer_a", predicate="location", value="Kisumu", provenance="user_stated"))

    results = store.get_facts_by_predicate("grows")
    assert len(results) == 2
    subjects = {fact.subject for fact in results}
    assert subjects == {"farmer_a", "farmer_b"}


def test_get_facts_by_predicate_returns_empty_when_none_match(tmp_path):
    db_file = tmp_path / "test_facts.db"
    store = FactStore(db_path=str(db_file))
    assert store.get_facts_by_predicate("nonexistent_predicate") == []


def test_get_facts_with_value_returns_all_matching_facts(tmp_path):
    db_file = tmp_path / "test_facts.db"
    store = FactStore(db_path=str(db_file))

    store.add_fact(Fact(subject="farmer_a", predicate="location", value="Nairobi", provenance="user_stated"))
    store.add_fact(Fact(subject="cooperative_x", predicate="based_in", value="Nairobi", provenance="user_stated"))
    store.add_fact(Fact(subject="farmer_b", predicate="location", value="Kisumu", provenance="user_stated"))

    results = store.get_facts_with_value("Nairobi")
    assert len(results) == 2
    subjects = {fact.subject for fact in results}
    assert subjects == {"farmer_a", "cooperative_x"}


def test_get_facts_with_value_returns_empty_when_none_match(tmp_path):
    db_file = tmp_path / "test_facts.db"
    store = FactStore(db_path=str(db_file))
    assert store.get_facts_with_value("nonexistent_value") == []


def test_get_related_single_hop(tmp_path):
    db_file = tmp_path / "test_facts.db"
    store = FactStore(db_path=str(db_file))

    store.add_fact(Fact(subject="farmer_a", predicate="member_of", value="cooperative_x", provenance="user_stated"))
    store.add_fact(Fact(subject="cooperative_x", predicate="based_in", value="Nairobi", provenance="user_stated"))

    results = store.get_related("farmer_a", max_depth=1)
    assert len(results) == 1
    assert results[0].value == "cooperative_x"


def test_get_related_two_hops(tmp_path):
    db_file = tmp_path / "test_facts.db"
    store = FactStore(db_path=str(db_file))

    store.add_fact(Fact(subject="farmer_a", predicate="member_of", value="cooperative_x", provenance="user_stated"))
    store.add_fact(Fact(subject="cooperative_x", predicate="based_in", value="Nairobi", provenance="user_stated"))

    results = store.get_related("farmer_a", max_depth=2)
    assert len(results) == 2
    values = {fact.value for fact in results}
    assert values == {"cooperative_x", "Nairobi"}


def test_get_related_is_cycle_safe(tmp_path):
    db_file = tmp_path / "test_facts.db"
    store = FactStore(db_path=str(db_file))

    store.add_fact(Fact(subject="a", predicate="linked_to", value="b", provenance="user_stated"))
    store.add_fact(Fact(subject="b", predicate="linked_to", value="a", provenance="user_stated"))

    results = store.get_related("a", max_depth=5)
    assert len(results) == 2


def test_get_related_returns_empty_for_unrelated_subject(tmp_path):
    db_file = tmp_path / "test_facts.db"
    store = FactStore(db_path=str(db_file))
    assert store.get_related("nonexistent_subject", max_depth=2) == []


def test_get_related_rejects_negative_depth(tmp_path):
    db_file = tmp_path / "test_facts.db"
    store = FactStore(db_path=str(db_file))
    try:
        store.get_related("anything", max_depth=-1)
        assert False, "expected ValueError"
    except ValueError:
        pass
