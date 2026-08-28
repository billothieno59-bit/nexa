import pytest

from core.perception.capture.audio_capturer import AudioPerceptionCapturer


def test_modality_is_audio():
    capturer = AudioPerceptionCapturer()
    assert capturer.modality == "audio"


def test_capture_valid_bytes():
    capturer = AudioPerceptionCapturer()
    event = capturer.capture(b"\x00\x01\x02", source="mic")
    assert event.modality == "audio"
    assert event.source == "mic"
    assert event.payload == b"\x00\x01\x02"
    assert event.metadata["byte_length"] == 3


def test_capture_rejects_non_bytes():
    capturer = AudioPerceptionCapturer()
    with pytest.raises(TypeError):
        capturer.capture("not bytes", source="mic")


def test_capture_rejects_empty_bytes():
    capturer = AudioPerceptionCapturer()
    with pytest.raises(ValueError):
        capturer.capture(b"", source="mic")
