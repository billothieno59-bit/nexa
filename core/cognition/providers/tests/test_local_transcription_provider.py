"""
NEXA NexaLocalTranscriptionProvider Tests. Fully offline.
"""

from core.cognition.providers.local_transcription_provider import NexaLocalTranscriptionProvider
from core.perception.events import PerceptionEvent


def _audio_event(payload=b"\x00\x01"):
    return PerceptionEvent(modality="audio", source="mic", payload=payload, metadata={})


def test_provider_name():
    provider = NexaLocalTranscriptionProvider()
    assert provider.provider_name == "nexa_local"


def test_transcribe_rejects_non_audio_event():
    provider = NexaLocalTranscriptionProvider()
    event = PerceptionEvent(modality="image", source="camera", payload=b"\x01", metadata={})
    result = provider.transcribe(event)
    assert result["status"] == "rejected"


def test_transcribe_returns_not_implemented_honestly():
    provider = NexaLocalTranscriptionProvider()
    result = provider.transcribe(_audio_event())
    assert result["status"] == "not_implemented"
    assert result["provider"] == "nexa_local"
    assert "message" in result
