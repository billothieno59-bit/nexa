"""
NEXA Africa Operating System
File: core/perception/capture/audio_capturer.py
Constitutional Owner: Bill Odhiambo Othieno
Description: PerceptionCapturer for raw audio bytes. Structures input
             only — does not transcribe or interpret. Speech-to-text
             is a separate, not-yet-built provider concern.
"""

from __future__ import annotations

from core.perception.capture.base import PerceptionCapturer
from core.perception.events import PerceptionEvent
from core.services.logging.logger import get_logger

logger = get_logger(__name__)


class AudioPerceptionCapturer(PerceptionCapturer):
    """
    Captures raw audio bytes as a PerceptionEvent.

    Does not transcribe or interpret the audio — only validates and
    structures it, per the UPL contract. Transcription/understanding
    is a future provider concern, not part of this capturer.
    """

    @property
    def modality(self) -> str:
        return "audio"

    def capture(self, raw_input: object, source: str) -> PerceptionEvent:
        if not isinstance(raw_input, (bytes, bytearray)):
            raise TypeError(
                "AudioPerceptionCapturer.capture() requires bytes or bytearray raw_input."
            )

        if len(raw_input) == 0:
            raise ValueError(
                "AudioPerceptionCapturer.capture() received empty audio data."
            )

        logger.info("Captured audio perception event from source=%s", source)

        return PerceptionEvent(
            modality=self.modality,
            source=source,
            payload=bytes(raw_input),
            metadata={"byte_length": len(raw_input)},
        )


__all__ = [
    "AudioPerceptionCapturer",
]
