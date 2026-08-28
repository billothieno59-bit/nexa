"""
NEXA OpenAITranscriptionProvider Tests. No real network calls.
"""

from core.cognition.providers.openai_transcription_provider import OpenAITranscriptionProvider
from core.perception.events import PerceptionEvent


class _FakeTranscriptionResponse:
    def __init__(self, text):
        self.text = text


class _FakeAudioNamespace:
    def __init__(self, response_text):
        self.transcriptions = self
        self._response_text = response_text

    def create(self, **kwargs):
        return _FakeTranscriptionResponse(self._response_text)


class _FakeClient:
    def __init__(self, response_text="fake transcript"):
        self.audio = _FakeAudioNamespace(response_text)


def _audio_event(payload=b"\x00\x01\x02"):
    return PerceptionEvent(modality="audio", source="mic", payload=payload, metadata={})


def test_provider_name():
    provider = OpenAITranscriptionProvider(client=_FakeClient())
    assert provider.provider_name == "openai"


def test_transcribe_rejects_non_audio_event():
    provider = OpenAITranscriptionProvider(client=_FakeClient())
    event = PerceptionEvent(modality="text", source="cli", payload="hi", metadata={})
    result = provider.transcribe(event)
    assert result["status"] == "rejected"


def test_transcribe_rejects_empty_payload():
    provider = OpenAITranscriptionProvider(client=_FakeClient())
    result = provider.transcribe(_audio_event(payload=b""))
    assert result["status"] == "rejected"


def test_transcribe_without_key_not_configured(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    provider = OpenAITranscriptionProvider(client=None)
    result = provider.transcribe(_audio_event())
    assert result["status"] == "not_configured"


def test_transcribe_success():
    provider = OpenAITranscriptionProvider(client=_FakeClient(response_text="hujambo nexa"))
    result = provider.transcribe(_audio_event())
    assert result["status"] == "ok"
    assert result["text"] == "hujambo nexa"
    assert result["provider"] == "openai"
