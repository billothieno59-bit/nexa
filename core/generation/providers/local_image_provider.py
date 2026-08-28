"""
NEXA Africa Operating System
File: core/generation/providers/local_image_provider.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Reserved seam for NEXA's own, locally-trained image
             generation model. NOT implemented yet — training a real
             image model requires funding (data + compute), per
             docs/roadmap/FUNDING_TIER.md. This class exists now so that
             once a real model is trained, only this file's generate()
             method needs real logic — no skill, permission, or test
             calling it has to change. Returns "not_implemented"
             honestly rather than fabricating a fake image result.
"""

from __future__ import annotations

from typing import Any, Dict

from core.generation.providers.base import ImageGenerationProvider


class NexaLocalImageProvider(ImageGenerationProvider):
    """
    Placeholder for NEXA's own future local image generation model.
    Deliberately does not fabricate output.
    """

    @property
    def provider_name(self) -> str:
        return "nexa_local"

    def generate(self, prompt: str, size: str = "1024x1024") -> Dict[str, Any]:
        if not isinstance(prompt, str) or not prompt.strip():
            return {"status": "rejected", "error": "prompt must be a non-empty string."}

        return {
            "status": "not_implemented",
            "provider": self.provider_name,
            "message": (
                "NEXA does not yet have its own trained image generation model. "
                "This requires funding for training data and compute — "
                "see docs/roadmap/FUNDING_TIER.md."
            ),
        }


__all__ = ["NexaLocalImageProvider"]
