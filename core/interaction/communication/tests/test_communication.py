"""
NEXA Africa Operating System
File: core/interaction/communication/tests/test_communication.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Unit tests for the Universal Communication Layer language registry and modern Sheng adapter.
"""

from core.interaction.communication.registry.language_registry import global_language_registry
from core.interaction.communication.adapters.sheng_adapter import default_sheng_adapter


def test_language_registry_initialization() -> None:
    """Verifies that the global language registry boots with the correct baseline profiles."""
    variants = global_language_registry.fetch_active_variants()
    assert "sw_KE" in variants
    assert "sheng_variety" in variants


def test_modern_sheng_normalization() -> None:
    """Verifies that modern contemporary Sheng tokens map accurately to standardized Swahili."""
    rada_test = default_sheng_adapter.normalize_input_phrase("rada")
    assert rada_test["normalized_swahili_target"] == "hali gani"
    assert rada_test["translation_applied"] is True
    assert rada_test["safety_governance_passed"] is True

    ganji_test = default_sheng_adapter.normalize_input_phrase("ganji")
    assert ganji_test["normalized_swahili_target"] == "pesa"


def test_unmapped_token_passthrough() -> None:
    """Verifies that unfamiliar terms pass through safely without modification or errors."""
    unknown_phrase = "random_word_xyz"
    test_run = default_sheng_adapter.normalize_input_phrase(unknown_phrase)
    assert test_run["normalized_swahili_target"] == unknown_phrase
    assert test_run["translation_applied"] is False
