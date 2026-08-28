"""
NEXA AnthropicVisionProvider Tests. No real network calls.
"""

from core.cognition.providers.anthropic_vision_provider import AnthropicVisionProvider
from core.perception.events import PerceptionEvent


class _FakeContentBlock:
    def __init__(self, text):
        self.text = text


class _FakeResponse:
    def __init__(self, text):
        self.content = [_FakeContentBlock(text)]


class _FakeClient:
    def __init__(self, response_text="fake description"):
        self._response_text = response_text
        self.messages = self

    def create(self, **kwargs):
        return _FakeResponse(self._response_text)


def _image_event(payload=b"\xff\xd8\xff"):
    return PerceptionEvent(modality="image", source="camera", payload=payload, metadata={})


def test_provider_name():
    provider = AnthropicVisionProvider(client=_FakeClient())
    assert provider.provider_name == "anthropic"


def test_describe_rejects_non_image_event():
    provider = AnthropicVisionProvider(client=_FakeClient())
    event = PerceptionEvent(modality="audio", source="mic", payload=b"\x01", metadata={})
    result = provider.describe(event)
    assert result["status"] == "rejected"


def test_describe_rejects_empty_payload():
    provider = AnthropicVisionProvider(client=_FakeClient())
    result = provider.describe(_image_event(payload=b""))
    assert result["status"] == "rejected"


def test_describe_without_key_not_configured(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    provider = AnthropicVisionProvider(client=None)
    result = provider.describe(_image_event())
    assert result["status"] == "not_configured"


def test_describe_success():
    provider = AnthropicVisionProvider(client=_FakeClient(response_text="a red bicycle"))
    result = provider.describe(_image_event())
    assert result["status"] == "ok"
    assert result["response"] == "a red bicycle"
    assert result["provider"] == "anthropic"
