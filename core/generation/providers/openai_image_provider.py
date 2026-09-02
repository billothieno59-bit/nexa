"""
NEXA Africa Operating System
File: core/generation/providers/openai_image_provider.py
Constitutional Owner: Bill Odhiambo Othieno
Description: ImageGenerationProvider backed by the real OpenAI API. Same
             logic previously inline in skills/privileged/image_generation.py,
             now behind the ImageGenerationProvider interface.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from core.generation.providers.base import ImageGenerationProvider
from core.services.logging.logger import get_logger

logger = get_logger(__name__)

DEFAULT_MODEL_ENV_VAR = "NEXA_IMAGE_MODEL"
DEFAULT_MODEL = "dall-e-3"
API_KEY_ENV_VAR = "OPENAI_API_KEY"


class OpenAIImageProvider(ImageGenerationProvider):
    def __init__(self, client: Optional[Any] = None, model: Optional[str] = None) -> None:
        self._injected_client = client
        self._model = model or os.environ.get(DEFAULT_MODEL_ENV_VAR, DEFAULT_MODEL)

    @property
    def provider_name(self) -> str:
        return "openai"

    def _get_client(self) -> Optional[Any]:
        if self._injected_client is not None:
            return self._injected_client
        api_key = os.environ.get(API_KEY_ENV_VAR)
        if not api_key:
            return None
        import openai  # imported lazily

        return openai.OpenAI(api_key=api_key)

    def generate(self, prompt: str, size: str = "1024x1024") -> Dict[str, Any]:
        if not isinstance(prompt, str) or not prompt.strip():
            return {"status": "rejected", "error": "prompt must be a non-empty string."}

        client = self._get_client()
        if client is None:
            logger.warning("OpenAI image generation requested but %s is not configured.", API_KEY_ENV_VAR)
            return {"status": "not_configured", "error": f"{API_KEY_ENV_VAR} is not set."}

        try:
            response = client.images.generate(model=self._model, prompt=prompt, size=size, n=1)
            image_url = response.data[0].url
            return {"status": "ok", "image_url": image_url, "model": self._model, "provider": self.provider_name}
        except Exception as exc:
            logger.exception("OpenAI image generation call failed.")
            return {"status": "error", "error": str(exc)}


__all__ = ["OpenAIImageProvider", "API_KEY_ENV_VAR", "DEFAULT_MODEL"]
