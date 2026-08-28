"""
NEXA AccessibilityProfile Tests.
"""

import pytest

from core.interaction.accessibility.profile import AccessibilityProfile


def test_profile_defaults_request_no_accommodation():
    profile = AccessibilityProfile(profile_id="user_1")
    assert profile.needs_simplified_language is False
    assert profile.needs_screen_reader_friendly_output is False
    assert profile.preferred_reading_level is None


def test_profile_rejects_empty_id():
    with pytest.raises(ValueError):
        AccessibilityProfile(profile_id="")


def test_profile_rejects_invalid_reading_level():
    with pytest.raises(ValueError):
        AccessibilityProfile(profile_id="user_1", preferred_reading_level="advanced")


def test_profile_is_immutable():
    profile = AccessibilityProfile(profile_id="user_1")
    with pytest.raises(Exception):
        profile.needs_simplified_language = True
