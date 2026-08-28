"""
NEXA NexaLocalVisionProvider Tests. Fully offline.
"""

from core.cognition.providers.local_vision_provider import NexaLocalVisionProvider
from core.perception.events import PerceptionEvent


def _image_event(payload=b"\x01\x02"):
    return PerceptionEvent(modality="image", source="camera", payload=payload, metadata={})


def test_provider_name():
    provider = NexaLocalVisionProvider()
    assert provider.provider_name == "nexa_local"


def test_describe_rejects_non_image_event():
    provider = NexaLocalVisionProvider()
    event = PerceptionEvent(modality="audio", source="mic", payload=b"\x01", metadata={})
    result = provider.describe(event)
    assert result["status"] == "rejected"


def test_describe_returns_not_implemented_honestly():
    provider = NexaLocalVisionProvider()
    result = provider.describe(_image_event())
    assert result["status"] == "not_implemented"
    assert result["provider"] == "nexa_local"
    assert "message" in result
