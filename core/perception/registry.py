"""
NEXA Africa Operating System
File: core/perception/registry.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Routes raw input to the correct PerceptionCapturer by modality,
             per core/contracts/perception/upl_contract_v1.md. New modalities
             (audio, image, sensor) register here without callers needing to
             know which concrete capturer class handles them.
"""

from __future__ import annotations

from typing import Dict

from core.perception.capture.audio_capturer import AudioPerceptionCapturer
from core.perception.capture.base import PerceptionCapturer
from core.perception.capture.image_capturer import ImagePerceptionCapturer
from core.perception.capture.sensor_capturer import SensorPerceptionCapturer
from core.perception.capture.text_capturer import TextPerceptionCapturer
from core.perception.events import PerceptionEvent
from core.services.logging.logger import get_logger

logger = get_logger(__name__)


class UnknownModalityError(Exception):
    """Raised when no capturer is registered for a requested modality."""


class PerceptionRegistry:
    """
    Registers PerceptionCapturers by modality and routes capture
    requests to the correct one.

    Unknown modalities fail closed (raise) rather than silently
    dropping input, consistent with the rest of the codebase.
    """

    def __init__(self) -> None:
        self._capturers: Dict[str, PerceptionCapturer] = {}

    def register(self, capturer: PerceptionCapturer) -> None:
        """
        Register a capturer under its own declared modality.
        """
        if not isinstance(capturer, PerceptionCapturer):
            raise TypeError(
                "PerceptionRegistry.register() requires a PerceptionCapturer."
            )

        self._capturers[capturer.modality] = capturer
        logger.info("Registered perception capturer for modality=%s", capturer.modality)

    def capture(self, modality: str, raw_input: object, source: str) -> PerceptionEvent:
        """
        Route raw input to the capturer registered for the given modality.

        Raises UnknownModalityError if no capturer is registered.
        """
        capturer = self._capturers.get(modality)

        if capturer is None:
            raise UnknownModalityError(
                f"No perception capturer registered for modality '{modality}'."
            )

        return capturer.capture(raw_input, source)

    def registered_modalities(self) -> tuple[str, ...]:
        """
        Return the modalities currently registered, for diagnostics.
        """
        return tuple(self._capturers.keys())


def _build_default_registry() -> PerceptionRegistry:
    registry = PerceptionRegistry()
    registry.register(TextPerceptionCapturer())
    registry.register(AudioPerceptionCapturer())
    registry.register(ImagePerceptionCapturer())
    registry.register(SensorPerceptionCapturer())
    return registry


global_perception_registry = _build_default_registry()


__all__ = [
    "PerceptionRegistry",
    "UnknownModalityError",
    "global_perception_registry",
]
