"""
NEXA Africa Operating System
File: core/perception/capture/text_capturer.py
Constitutional Owner: Bill Odhiambo Othieno
Description: The first concrete PerceptionCapturer. Structures raw text
             input into a PerceptionEvent. Audio/image/sensor capturers
             will implement the same PerceptionCapturer interface once
             those modalities are built.
"""

from __future__ import annotations

from core.perception.capture.base import PerceptionCapturer
from core.perception.events import PerceptionEvent
from core.services.logging.logger import get_logger

logger = get_logger(__name__)


class TextPerceptionCapturer(PerceptionCapturer):
    """
    Captures raw text input as a PerceptionEvent.

    This does not interpret language, dialect, or meaning — it only
    validates and structures the raw text, per the UPL contract.
    """

    @property
    def modality(self) -> str:
        return "text"

    def capture(self, raw_input: object, source: str) -> PerceptionEvent:
        if not isinstance(raw_input, str):
            raise TypeError("TextPerceptionCapturer.capture() requires a string raw_input.")

        if not raw_input.strip():
            raise ValueError("TextPerceptionCapturer.capture() received empty text.")

        logger.info("Captured text perception event from source=%s", source)

        return PerceptionEvent(
            modality=self.modality,
            source=source,
            payload=raw_input,
            metadata={"length": len(raw_input)},
        )


__all__ = [
    "TextPerceptionCapturer",
]
