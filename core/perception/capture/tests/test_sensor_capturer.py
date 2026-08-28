import pytest

from core.perception.capture.sensor_capturer import SensorPerceptionCapturer


def test_modality_is_sensor():
    capturer = SensorPerceptionCapturer()
    assert capturer.modality == "sensor"


def test_capture_valid_reading():
    capturer = SensorPerceptionCapturer()
    event = capturer.capture(
        {"reading_type": "soil_moisture", "value": 42.5},
        source="field_sensor_01",
    )
    assert event.modality == "sensor"
    assert event.payload["reading_type"] == "soil_moisture"
    assert event.payload["value"] == 42.5
    assert event.metadata["reading_type"] == "soil_moisture"


def test_capture_rejects_non_mapping():
    capturer = SensorPerceptionCapturer()
    with pytest.raises(TypeError):
        capturer.capture("not a mapping", source="field_sensor_01")


def test_capture_rejects_missing_keys():
    capturer = SensorPerceptionCapturer()
    with pytest.raises(ValueError):
        capturer.capture({"reading_type": "soil_moisture"}, source="field_sensor_01")
