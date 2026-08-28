"""
NEXA Transcription Provider Router Tests.
"""

from core.cognition.providers.transcription_router import get_transcription_provider
from core.cognition.providers.openai_transcription_provider import OpenAITranscriptionProvider
from core.cognition.providers.local_transcription_provider import NexaLocalTranscriptionProvider


def test_defaults_to_openai():
    provider = get_transcription_provider()
    assert isinstance(provider, OpenAITranscriptionProvider)


def test_explicit_local_selection():
    provider = get_transcription_provider("nexa_local")
    assert isinstance(provider, NexaLocalTranscriptionProvider)


def test_unknown_provider_falls_back_to_default():
    provider = get_transcription_provider("nonexistent_provider")
    assert isinstance(provider, OpenAITranscriptionProvider)
