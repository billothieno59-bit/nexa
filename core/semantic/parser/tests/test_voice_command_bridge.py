from core.perception.events import PerceptionEvent
from core.semantic.parser.voice_command_bridge import resolve_voice_command


class _FakeTranscriptionProvider:
    def __init__(self, result):
        self._result = result

    def transcribe(self, event, filename="audio.wav"):
        return self._result


def _audio_event(payload=b"\x00\x01"):
    return PerceptionEvent(modality="audio", source="mic", payload=payload, metadata={})


def test_rejects_non_audio_event():
    result = resolve_voice_command(
        PerceptionEvent(modality="text", source="cli", payload="hi", metadata={})
    )
    assert result["governed_execution_authorized"] is False
    assert result["transcription_status"] == "rejected"


def test_known_swahili_phrase_resolves_through_same_mapper_as_text():
    provider = _FakeTranscriptionProvider({"status": "ok", "text": "pesa", "provider": "fake"})
    result = resolve_voice_command(_audio_event(), transcription_provider=provider)
    assert result["resolved_intent_token"] == "INTENT_RESOURCE_VALUE_TRANSACT"
    assert result["governed_execution_authorized"] is True
    assert result["safety_status"] == "VERIFIED"
    assert result["transcribed_text"] == "pesa"


def test_unknown_phrase_fails_closed():
    provider = _FakeTranscriptionProvider({"status": "ok", "text": "gibberish nonsense", "provider": "fake"})
    result = resolve_voice_command(_audio_event(), transcription_provider=provider)
    assert result["resolved_intent_token"] == "INTENT_UNKNOWN_PASSTHROUGH"
    assert result["governed_execution_authorized"] is False
    assert result["safety_status"] == "CLOSED"


def test_transcription_not_configured_fails_closed_without_guessing():
    provider = _FakeTranscriptionProvider({"status": "not_configured", "error": "OPENAI_API_KEY is not set."})
    result = resolve_voice_command(_audio_event(), transcription_provider=provider)
    assert result["governed_execution_authorized"] is False
    assert result["transcription_status"] == "not_configured"
    assert "resolved_intent_token" not in result or result["resolved_intent_token"] == "INTENT_UNKNOWN_PASSTHROUGH"


def test_transcription_error_fails_closed():
    provider = _FakeTranscriptionProvider({"status": "error", "error": "network failure"})
    result = resolve_voice_command(_audio_event(), transcription_provider=provider)
    assert result["governed_execution_authorized"] is False
    assert result["transcription_status"] == "error"


def test_case_insensitive_matching_matches_text_behavior():
    provider = _FakeTranscriptionProvider({"status": "ok", "text": "  KAZI  ", "provider": "fake"})
    result = resolve_voice_command(_audio_event(), transcription_provider=provider)
    assert result["resolved_intent_token"] == "INTENT_PROCESS_EXECUTION_RUN"
