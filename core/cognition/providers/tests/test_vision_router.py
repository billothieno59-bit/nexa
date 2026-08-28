"""
NEXA Vision Provider Router Tests.
"""

from core.cognition.providers.vision_router import get_vision_provider
from core.cognition.providers.anthropic_vision_provider import AnthropicVisionProvider
from core.cognition.providers.local_vision_provider import NexaLocalVisionProvider


def test_defaults_to_anthropic():
    provider = get_vision_provider()
    assert isinstance(provider, AnthropicVisionProvider)


def test_explicit_local_selection():
    provider = get_vision_provider("nexa_local")
    assert isinstance(provider, NexaLocalVisionProvider)


def test_unknown_provider_falls_back_to_default():
    provider = get_vision_provider("nonexistent_provider")
    assert isinstance(provider, AnthropicVisionProvider)
