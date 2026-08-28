"""
NEXA Africa Operating System
File: core/cognition/providers/local_vision_provider.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Reserved seam for NEXA's own, locally-run vision
             understanding model. NOT implemented yet — a real local
             model requires funding (data + compute), per
             docs/roadmap/FUNDING_TIER.md. This class exists now so
             that once a real model is available, only this file's
             describe() method needs real logic — no skill, permission,
             or test calling it has to change. Returns
             "not_implemented" honestly rather than fabricating a fake
             description.
"""

from __future__ import annotations

from typing import Any, Dict

from core.cognition.providers.base import VisionUnderstandingProvider
from core.perception.events import PerceptionEvent


class NexaLocalVisionProvider(VisionUnderstandingProvider):
    """
    Placeholder for NEXA's own future local vision understanding
    model. Deliberately does not fabricate a description.
    """

    @property
    def provider_name(self) -> str:
        return "nexa_local"

    def describe(self, event: PerceptionEvent, prompt: str = "Describe this image.") -> Dict[str, Any]:
        if not isinstance(event, PerceptionEvent) or event.modality != "image":
            return {"status": "rejected", "error": "event must be a PerceptionEvent with modality='image'."}

        return {
            "status": "not_implemented",
            "provider": self.provider_name,
            "message": (
                "NEXA does not yet have its own trained vision understanding model. "
                "This requires funding for training data and compute — "
                "see docs/roadmap/FUNDING_TIER.md."
            ),
        }


__all__ = [
    "NexaLocalVisionProvider",
]
