import pytest

from core.perception.capture.image_capturer import ImagePerceptionCapturer


def test_modality_is_image():
    capturer = ImagePerceptionCapturer()
    assert capturer.modality == "image"


def test_capture_valid_bytes():
    capturer = ImagePerceptionCapturer()
    event = capturer.capture(b"\xff\xd8\xff", source="camera")
    assert event.modality == "image"
    assert event.source == "camera"
    assert event.payload == b"\xff\xd8\xff"
    assert event.metadata["byte_length"] == 3


def test_capture_rejects_non_bytes():
    capturer = ImagePerceptionCapturer()
    with pytest.raises(TypeError):
        capturer.capture("not bytes", source="camera")


def test_capture_rejects_empty_bytes():
    capturer = ImagePerceptionCapturer()
    with pytest.raises(ValueError):
        capturer.capture(b"", source="camera")
