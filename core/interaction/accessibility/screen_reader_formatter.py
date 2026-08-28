"""
NEXA Africa Operating System
File: core/interaction/accessibility/screen_reader_formatter.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Reformats text to be more screen-reader-friendly: expands
             common abbreviations and symbols into words a screen reader
             pronounces clearly, and removes decorative characters that
             screen readers otherwise read aloud awkwardly (e.g. "***").
             This is an honest, narrow transformation — it does not
             implement an actual screen reader or text-to-speech engine.
"""

from __future__ import annotations

import re

_EXPANSIONS = {
    "&": " and ",
    "%": " percent ",
    "#": " number ",
    "@": " at ",
    "w/": " with ",
    "e.g.": " for example ",
    "i.e.": " that is ",
    "etc.": " et cetera ",
}

_DECORATIVE_CHARS_PATTERN = re.compile(r"[*_~`]{2,}")


def format_for_screen_reader(text: str) -> str:
    """
    Expand common abbreviations/symbols and strip decorative character
    runs (e.g. markdown emphasis markers) so the result reads cleanly
    aloud. Does not summarize or reword sentences.
    """
    if not isinstance(text, str):
        raise TypeError("format_for_screen_reader() requires a string.")

    result = text
    result = _DECORATIVE_CHARS_PATTERN.sub("", result)

    for token, expansion in _EXPANSIONS.items():
        result = result.replace(token, expansion)

    result = re.sub(r"\s+", " ", result).strip()
    return result


__all__ = [
    "format_for_screen_reader",
]
