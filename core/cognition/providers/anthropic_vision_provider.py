"""
NEXA Africa Operating System
File: core/cognition/providers/anthropic_vision_provider.py
Constitutional Owner: Bill Odhiambo Othieno
Description: VisionUnderstandingProvider backed by the real Anthropic
             Claude API's image understanding. Consumes the
             PerceptionEvent produced by ImagePerceptionCapturer —
             never called directly by the capturer itself, keeping
             capture and interpretation as separate concerns per the
             UPL contract.

             Known limitation, stated honestly: ImagePerceptionCapturer
             does not currently detect or validate image encoding, so
             this provider assumes JPEG unless the caller specifies a
             different media_type.
"""

from __future__ import annotations

import base64
import os
from typing import Any, Dict, Optional

from core.cognition.providers.base import VisionUnderstandingProvider
from core.perception.events import PerceptionEvent
from core.services.logging.logger import get_logger

logger = get_logger(__name__)

DEFAULT_MODEL_ENV_VAR = "NEXA_VISION_MODEL"
DEFAULT_MODEL = "claude-sonnet-5"
API_KEY_ENV_VAR = "ANTHROPIC_API_KEY"
DEFAULT_MEDIA_TYPE = "image/jpeg"


class AnthropicVisionProvider(VisionUnderstandingProvider):
    """
    Wraps Anthropic Claude's image understanding behind the
    VisionUnderstandingProvider interface.
    """

    def __init__(self, client: Optional[Any] = None, model: Optional[str] = None) -> None:
        self._injected_client = client
        self._model = model or os.environ.get(DEFAULT_MODEL_ENV_VAR, DEFAULT_MODEL)

    @property
    def provider_name(self) -> str:
        return "anthropic"

    def _get_client(self) -> Optional[Any]:
        if self._injected_client is not None:
            return self._injected_client

        api_key = os.environ.get(API_KEY_ENV_VAR)
        if not api_key:
            return None

        import anthropic  # imported lazily

        return anthropic.Anthropic(api_key=api_key)

    def describe(
        self,
        event: PerceptionEvent,
        prompt: str = "Describe this image.",
        media_type: str = DEFAULT_MEDIA_TYPE,
    ) -> Dict[str, Any]:
        if not isinstance(event, PerceptionEvent) or event.modality != "image":
            return {"status": "rejected", "error": "event must be a PerceptionEvent with modality='image'."}

        image_bytes = event.payload
        if not isinstance(image_bytes, (bytes, bytearray)) or len(image_bytes) == 0:
            return {"status": "rejected", "error": "event.payload must be non-empty bytes."}

        client = self._get_client()
        if client is None:
            logger.warning("Anthropic vision requested but %s is not configured.", API_KEY_ENV_VAR)
            return {"status": "not_configured", "error": f"{API_KEY_ENV_VAR} is not set."}

        try:
            encoded = base64.standard_b64encode(bytes(image_bytes)).decode("utf-8")
            response = client.messages.create(
                model=self._model,
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {"type": "base64", "media_type": media_type, "data": encoded},
                            },
                            {"type": "text", "text": prompt},
                        ],
                    }
                ],
            )
            text = response.content[0].text
            return {"status": "ok", "response": text, "model": self._model, "provider": self.provider_name}
        except Exception as exc:
            logger.exception("Anthropic vision call failed.")
            return {"status": "error", "error": str(exc)}


__all__ = [
    "AnthropicVisionProvider",
    "API_KEY_ENV_VAR",
    "DEFAULT_MODEL",
    "DEFAULT_MEDIA_TYPE",
]
