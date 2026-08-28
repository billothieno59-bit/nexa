"""
NEXA AnthropicReasoningProvider Tests. No real network calls.
"""

from core.cognition.providers.anthropic_provider import AnthropicReasoningProvider


class _FakeContentBlock:
    def __init__(self, text):
        self.text = text


class _FakeResponse:
    def __init__(self, text):
        self.content = [_FakeContentBlock(text)]


class _FakeClient:
    def __init__(self, response_text="fake"):
        self._response_text = response_text
        self.messages = self

    def create(self, **kwargs):
        return _FakeResponse(self._response_text)


def test_provider_name():
    provider = AnthropicReasoningProvider(client=_FakeClient())
    assert provider.provider_name == "anthropic"


def test_reason_rejects_empty_prompt():
    provider = AnthropicReasoningProvider(client=_FakeClient())
    result = provider.reason("")
    assert result["status"] == "rejected"


def test_reason_without_key_not_configured(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    provider = AnthropicReasoningProvider(client=None)
    result = provider.reason("hello")
    assert result["status"] == "not_configured"


def test_reason_success():
    provider = AnthropicReasoningProvider(client=_FakeClient(response_text="42"))
    result = provider.reason("what is the answer")
    assert result["status"] == "ok"
    assert result["response"] == "42"
