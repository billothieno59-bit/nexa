"""
NEXA Africa Operating System
File: core/generation/providers/local_voice_provider.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Reserved seam for NEXA's own, locally-trained voice
             generation model. NOT implemented yet — see
             docs/roadmap/FUNDING_TIER.md. Returns "not_implemented"
             honestly rather than fabricating fake audio.
"""

from __future__ import annotations

from typing import Any, Dict

from core.generation.providers.base import VoiceGenerationProvider


class NexaLocalVoiceProvider(VoiceGenerationProvider):
    """
    Placeholder for NEXA's own future local voice generation model.
    Deliberately does not fabricate output.
    """

    @property
    def provider_name(self) -> str:
        return "nexa_local"

    def generate(self, text: str) -> Dict[str, Any]:
        if not isinstance(text, str) or not text.strip():
            return {"status": "rejected", "error": "text must be a non-empty string."}

        return {
            "status": "not_implemented",
            "provider": self.provider_name,
            "message": (
                "NEXA does not yet have its own trained voice generation model. "
                "This requires funding for training data and compute — "
                "see docs/roadmap/FUNDING_TIER.md."
            ),
        }


__all__ = ["NexaLocalVoiceProvider"]
