"""
NEXA Text Perception Capturer Tests.
"""

import pytest

from core.perception.capture.text_capturer import TextPerceptionCapturer
from core.perception.events import PerceptionEvent


def test_capture_returns_perception_event():
    capturer = TextPerceptionCapturer()
    event = capturer.capture("niko fiti", source="cli")

    assert isinstance(event, PerceptionEvent)
    assert event.modality == "text"
    assert event.source == "cli"
    assert event.payload == "niko fiti"
    assert event.metadata["length"] == len("niko fiti")


def test_capture_rejects_non_string_input():
    capturer = TextPerceptionCapturer()
    with pytest.raises(TypeError):
        capturer.capture(12345, source="cli")


def test_capture_rejects_empty_string():
    capturer = TextPerceptionCapturer()
    with pytest.raises(ValueError):
        capturer.capture("   ", source="cli")


def test_perception_event_is_immutable():
    capturer = TextPerceptionCapturer()
    event = capturer.capture("test", source="cli")

    with pytest.raises(Exception):
        event.payload = "changed"


def test_perception_event_rejects_empty_modality_or_source():
    from core.perception.events import PerceptionEvent

    with pytest.raises(ValueError):
        PerceptionEvent(modality="", source="cli", payload="x")

    with pytest.raises(ValueError):
        PerceptionEvent(modality="text", source="", payload="x")
