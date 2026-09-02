from __future__ import annotations

from typing import Any, Dict

from core.perception.events import PerceptionEvent


class NexaLocalTranscriptionProvider:
    """
    Reserved local speech-to-text provider for Phase 3.

    Honest placeholder:
    - Rejects non-audio perception events.
    - Returns not_implemented for valid audio events until
      NEXA's local transcription engine is integrated.
    """

    provider_name = "nexa_local"

    def transcribe(self, event: PerceptionEvent) -> Dict[str, Any]:
        if not isinstance(event, PerceptionEvent):
            return {
                "status": "rejected",
                "error": "Input must be a PerceptionEvent.",
            }

        if event.modality != "audio":
            return {
                "status": "rejected",
                "error": "Only audio perception events are supported.",
            }

        return {
            "status": "not_implemented",
            "provider": self.provider_name,
            "text": None,
            "message": "Local transcription engine has not been implemented yet.",
            "error": "Local transcription engine has not been implemented yet.",
        }


__all__ = ["NexaLocalTranscriptionProvider"]
