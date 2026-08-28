"""
NEXA Africa Operating System
File: core/interaction/accessibility/text_simplifier.py
Constitutional Owner: Bill Odhiambo Othieno
Description: A modest, honest text simplification adapter. It splits long
             sentences at existing punctuation and does not claim to do
             anything more sophisticated than that. This is intentionally
             narrow scope — real cognitive-accessibility text simplification
             is a much larger problem this does not attempt to solve.
"""

from __future__ import annotations

import re

MAX_WORDS_PER_SENTENCE = 15


def simplify_for_accessibility(text: str) -> str:
    """
    Break long sentences into shorter ones at existing commas, where
    a sentence exceeds MAX_WORDS_PER_SENTENCE words.

    This is a narrow, honest transformation: it does not rewrite
    vocabulary, does not summarize, and does not use any language
    model. It only restructures sentence length using punctuation
    already present in the text.
    """
    if not isinstance(text, str):
        raise TypeError("simplify_for_accessibility() requires a string.")

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    simplified_sentences = []

    for sentence in sentences:
        words = sentence.split()
        if len(words) <= MAX_WORDS_PER_SENTENCE:
            simplified_sentences.append(sentence)
            continue

        parts = sentence.split(", ")
        simplified_sentences.extend(p.strip() for p in parts if p.strip())

    return " ".join(simplified_sentences)


__all__ = [
    "simplify_for_accessibility",
    "MAX_WORDS_PER_SENTENCE",
]
