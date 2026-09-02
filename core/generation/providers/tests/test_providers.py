"""
NEXA Generation Provider Tests. No real network calls.
"""

from core.generation.providers.openai_image_provider import OpenAIImageProvider
from core.generation.providers.elevenlabs_voice_provider import ElevenLabsVoiceProvider
from core.generation.providers.local_image_provider import NexaLocalImageProvider
from core.generation.providers.local_voice_provider import NexaLocalVoiceProvider
from core.generation.providers.image_router import get_image_provider
from core.generation.providers.voice_router import get_voice_provider


class _FakeImageClient:
    class images:
        @staticmethod
        def generate(**kwargs):
            class R:
                data = [type("D", (), {"url": "https://fake.example/x.png"})()]

            return R()


class _FakeVoiceClient:
    def generate(self, **kwargs):
        return b"12345"


def test_openai_provider_success():
    provider = OpenAIImageProvider(client=_FakeImageClient())
    result = provider.generate("a bird")
    assert result["status"] == "ok"
    assert result["provider"] == "openai"


def test_elevenlabs_provider_success():
    provider = ElevenLabsVoiceProvider(client=_FakeVoiceClient())
    result = provider.generate("hello")
    assert result["status"] == "ok"
    assert result["provider"] == "elevenlabs"


def test_local_image_provider_returns_not_implemented_honestly():
    provider = NexaLocalImageProvider()
    result = provider.generate("a bird")
    assert result["status"] == "not_implemented"
    assert result["provider"] == "nexa_local"


def test_local_voice_provider_returns_not_implemented_honestly():
    provider = NexaLocalVoiceProvider()
    result = provider.generate("hello")
    assert result["status"] == "not_implemented"
    assert result["provider"] == "nexa_local"


def test_image_router_defaults_to_openai():
    assert isinstance(get_image_provider(), OpenAIImageProvider)


def test_image_router_selects_local():
    assert isinstance(get_image_provider("nexa_local"), NexaLocalImageProvider)


def test_voice_router_defaults_to_elevenlabs():
    assert isinstance(get_voice_provider(), ElevenLabsVoiceProvider)


def test_voice_router_selects_local():
    assert isinstance(get_voice_provider("nexa_local"), NexaLocalVoiceProvider)
