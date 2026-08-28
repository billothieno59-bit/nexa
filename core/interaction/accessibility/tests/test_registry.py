"""
NEXA AccessibilityProfileRegistry Tests.
"""

import pytest

from core.interaction.accessibility.registry import AccessibilityProfileRegistry
from core.interaction.accessibility.profile import AccessibilityProfile


def test_register_and_get_profile():
    registry = AccessibilityProfileRegistry()
    profile = AccessibilityProfile(profile_id="user_1", needs_simplified_language=True)

    registry.register(profile)
    retrieved = registry.get("user_1")

    assert retrieved == profile


def test_get_unknown_profile_returns_none():
    registry = AccessibilityProfileRegistry()
    assert registry.get("nonexistent") is None


def test_remove_profile():
    registry = AccessibilityProfileRegistry()
    profile = AccessibilityProfile(profile_id="user_1")
    registry.register(profile)

    assert registry.remove("user_1") is True
    assert registry.get("user_1") is None
    assert registry.remove("user_1") is False


def test_register_rejects_non_profile():
    registry = AccessibilityProfileRegistry()
    with pytest.raises(TypeError):
        registry.register("not a profile")
