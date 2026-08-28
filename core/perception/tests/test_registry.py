"""
NEXA Perception Registry Tests.
"""

import pytest

from core.perception.registry import (
    PerceptionRegistry,
    UnknownModalityError,
    global_perception_registry,
)
from core.perception.capture.audio_capturer import AudioPerceptionCapturer
from core.perception.capture.image_capturer import ImagePerceptionCapturer
from core.perception.capture.sensor_capturer import SensorPerceptionCapturer
from core.perception.capture.text_capturer import TextPerceptionCapturer
from core.perception.events import PerceptionEvent


def test_register_and_capture_routes_to_correct_capturer():
    registry = PerceptionRegistry()
    registry.register(TextPerceptionCapturer())

    event = registry.capture("text", "hujambo", source="cli")

    assert isinstance(event, PerceptionEvent)
    assert event.modality == "text"


def test_unregistered_modality_fails_closed():
    registry = PerceptionRegistry()

    with pytest.raises(UnknownModalityError):
        registry.capture("audio", b"raw bytes", source="microphone")


def test_register_rejects_non_capturer():
    registry = PerceptionRegistry()

    with pytest.raises(TypeError):
        registry.register("not a capturer")


def test_registered_modalities_reports_correctly():
    registry = PerceptionRegistry()
    assert registry.registered_modalities() == ()

    registry.register(TextPerceptionCapturer())
    assert registry.registered_modalities() == ("text",)


def test_global_registry_has_text_capturer_by_default():
    assert "text" in global_perception_registry.registered_modalities()

    event = global_perception_registry.capture("text", "niaje", source="cli")
    assert event.payload == "niaje"


def test_global_registry_has_all_four_modalities():
    modalities = global_perception_registry.registered_modalities()
    assert "text" in modalities
    assert "audio" in modalities
    assert "image" in modalities
    assert "sensor" in modalities


def test_global_registry_routes_audio():
    event = global_perception_registry.capture("audio", b"\x00\x01", source="mic")
    assert event.modality == "audio"
    assert event.payload == b"\x00\x01"


def test_global_registry_routes_image():
    event = global_perception_registry.capture("image", b"\xff\xd8", source="camera")
    assert event.modality == "image"
    assert event.payload == b"\xff\xd8"


def test_global_registry_routes_sensor():
    event = global_perception_registry.capture(
        "sensor",
        {"reading_type": "temperature", "value": 28.4},
        source="field_sensor_02",
    )
    assert event.modality == "sensor"
    assert event.payload["reading_type"] == "temperature"


def test_register_and_capture_audio_on_fresh_registry():
    registry = PerceptionRegistry()
    registry.register(AudioPerceptionCapturer())
    event = registry.capture("audio", b"\x01\x02", source="mic")
    assert event.modality == "audio"


def test_register_and_capture_image_on_fresh_registry():
    registry = PerceptionRegistry()
    registry.register(ImagePerceptionCapturer())
    event = registry.capture("image", b"\x01\x02", source="camera")
    assert event.modality == "image"


def test_register_and_capture_sensor_on_fresh_registry():
    registry = PerceptionRegistry()
    registry.register(SensorPerceptionCapturer())
    event = registry.capture(
        "sensor", {"reading_type": "humidity", "value": 61}, source="sensor_x"
    )
    assert event.modality == "sensor"
