"""
NEXA Provider Router Tests.
"""

from core.cognition.providers.router import get_reasoning_provider
from core.cognition.providers.anthropic_provider import AnthropicReasoningProvider
from core.cognition.providers.local_provider import NexaLocalProvider


def test_defaults_to_anthropic():
    provider = get_reasoning_provider()
    assert isinstance(provider, AnthropicReasoningProvider)


def test_explicit_local_selection():
    provider = get_reasoning_provider("nexa_local")
    assert isinstance(provider, NexaLocalProvider)


def test_unknown_provider_falls_back_to_default():
    provider = get_reasoning_provider("nonexistent_provider")
    assert isinstance(provider, AnthropicReasoningProvider)
