"""
NEXA Africa Operating System
File: core/generation/providers/image_router.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Selects an ImageGenerationProvider by configuration.
             Defaults to OpenAI today; NEXA_IMAGE_PROVIDER=nexa_local
             reserves the seam for a future funded local model.
"""

from __future__ import annotations

import os
from typing import Optional

from core.generation.providers.base import ImageGenerationProvider
from core.generation.providers.openai_image_provider import OpenAIImageProvider
from core.generation.providers.local_image_provider import NexaLocalImageProvider

PROVIDER_ENV_VAR = "NEXA_IMAGE_PROVIDER"
DEFAULT_PROVIDER = "openai"


def get_image_provider(name: Optional[str] = None) -> ImageGenerationProvider:
    selected = name or os.environ.get(PROVIDER_ENV_VAR, DEFAULT_PROVIDER)

    if selected == "nexa_local":
        return NexaLocalImageProvider()

    return OpenAIImageProvider()


__all__ = ["get_image_provider", "PROVIDER_ENV_VAR", "DEFAULT_PROVIDER"]
