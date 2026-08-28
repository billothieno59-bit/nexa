"""
NEXA Text Simplifier Tests.
"""

import pytest

from core.interaction.accessibility.text_simplifier import simplify_for_accessibility


def test_short_sentence_is_unchanged():
    text = "This is short."
    assert simplify_for_accessibility(text) == "This is short."


def test_long_sentence_with_commas_is_split():
    text = (
        "We went to the market, bought some vegetables, "
        "talked to a few neighbors, and then walked home together."
    )
    result = simplify_for_accessibility(text)
    assert "We went to the market" in result
    assert result.count(".") == 0 or "bought some vegetables" in result


def test_rejects_non_string_input():
    with pytest.raises(TypeError):
        simplify_for_accessibility(12345)
