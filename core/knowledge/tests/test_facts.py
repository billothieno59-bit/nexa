"""
NEXA Fact Tests.
"""

import pytest

from core.knowledge.facts import Fact


def test_valid_fact():
    fact = Fact(subject="nexa", predicate="is_a", value="operating system", provenance="user_stated")
    assert fact.subject == "nexa"


def test_rejects_empty_subject():
    with pytest.raises(ValueError):
        Fact(subject="", predicate="is_a", value="x", provenance="user_stated")


def test_fact_is_immutable():
    fact = Fact(subject="nexa", predicate="is_a", value="os", provenance="user_stated")
    with pytest.raises(Exception):
        fact.value = "changed"
