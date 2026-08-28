"""
NEXA Screen Reader Formatter Tests.
"""

import pytest

from core.interaction.accessibility.screen_reader_formatter import (
    format_for_screen_reader,
)


def test_expands_ampersand():
    assert format_for_screen_reader("bread & butter") == "bread and butter"


def test_expands_percent():
    assert format_for_screen_reader("50%") == "50 percent"


def test_strips_decorative_markers():
    assert format_for_screen_reader("**important**") == "important"


def test_rejects_non_string_input():
    with pytest.raises(TypeError):
        format_for_screen_reader(123)


def test_collapses_extra_whitespace():
    result = format_for_screen_reader("hello    world")
    assert result == "hello world"
