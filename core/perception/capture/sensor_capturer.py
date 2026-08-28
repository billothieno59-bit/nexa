"""
NEXA Africa Operating System
File: core/perception/capture/sensor_capturer.py
Constitutional Owner: Bill Odhiambo Othieno
Description: PerceptionCapturer for structured sensor readings (e.g.
             soil moisture, temperature). Unlike audio/image, sensor
             input arrives already structured, so no separate provider
             is needed to make sense of it.
"""

from __future__ import annotations

from typing import Mapping

from core.perception.capture.base import PerceptionCapturer
from core.perception.events import PerceptionEvent
from core.services.logging.logger import get_logger

logger = get_logger(__name__)


class SensorPerceptionCapturer(PerceptionCapturer):
    """
    Captures a structured sensor reading as a PerceptionEvent.

    raw_input must be a mapping with at least 'reading_type' and
    'value' keys. Unlike audio/image, sensor data arrives already
    structured, so no separate interpretation provider is required.
    """

    @property
    def modality(self) -> str:
        return "sensor"

    def capture(self, raw_input: object, source: str) -> PerceptionEvent:
        if not isinstance(raw_input, Mapping):
            raise TypeError(
                "SensorPerceptionCapturer.capture() requires a mapping raw_input."
            )

        if "reading_type" not in raw_input or "value" not in raw_input:
            raise ValueError(
                "SensorPerceptionCapturer.capture() requires 'reading_type' and 'value' keys."
            )

        logger.info(
            "Captured sensor perception event from source=%s reading_type=%s",
            source,
            raw_input["reading_type"],
        )

        return PerceptionEvent(
            modality=self.modality,
            source=source,
            payload=dict(raw_input),
            metadata={"reading_type": raw_input["reading_type"]},
        )


__all__ = [
    "SensorPerceptionCapturer",
]
