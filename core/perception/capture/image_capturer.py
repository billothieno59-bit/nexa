"""
NEXA Africa Operating System
File: core/perception/capture/image_capturer.py
Constitutional Owner: Bill Odhiambo Othieno
Description: PerceptionCapturer for raw image bytes. Structures input
             only — does not perform vision understanding. That is a
             separate, not-yet-built provider concern.
"""

from __future__ import annotations

from core.perception.capture.base import PerceptionCapturer
from core.perception.events import PerceptionEvent
from core.services.logging.logger import get_logger

logger = get_logger(__name__)


class ImagePerceptionCapturer(PerceptionCapturer):
    """
    Captures raw image bytes as a PerceptionEvent.

    Does not perform vision understanding — only validates and
    structures the raw bytes, per the UPL contract.
    """

    @property
    def modality(self) -> str:
        return "image"

    def capture(self, raw_input: object, source: str) -> PerceptionEvent:
        if not isinstance(raw_input, (bytes, bytearray)):
            raise TypeError(
                "ImagePerceptionCapturer.capture() requires bytes or bytearray raw_input."
            )

        if len(raw_input) == 0:
            raise ValueError(
                "ImagePerceptionCapturer.capture() received empty image data."
            )

        logger.info("Captured image perception event from source=%s", source)

        return PerceptionEvent(
            modality=self.modality,
            source=source,
            payload=bytes(raw_input),
            metadata={"byte_length": len(raw_input)},
        )


__all__ = [
    "ImagePerceptionCapturer",
]
