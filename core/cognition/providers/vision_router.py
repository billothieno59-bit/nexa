"""
NEXA Africa Operating System
File: core/cognition/providers/vision_router.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Selects a VisionUnderstandingProvider by configuration.
             Defaults to the real Anthropic provider today; switching
             NEXA_VISION_PROVIDER to "nexa_local" reserves the seam for
             a future funded local model, with no code changes to any
             caller.
"""

from __future__ import annotations

import os
from typing import Optional

from core.cognition.providers.base import VisionUnderstandingProvider
from core.cognition.providers.anthropic_vision_provider import AnthropicVisionProvider
from core.cognition.providers.local_vision_provider import NexaLocalVisionProvider

PROVIDER_ENV_VAR = "NEXA_VISION_PROVIDER"
DEFAULT_PROVIDER = "anthropic"


def get_vision_provider(name: Optional[str] = None) -> VisionUnderstandingProvider:
    """
    Return the configured VisionUnderstandingProvider. Unknown names
    fail closed by falling back to the default rather than silently
    returning None.
    """
    selected = name or os.environ.get(PROVIDER_ENV_VAR, DEFAULT_PROVIDER)

    if selected == "nexa_local":
        return NexaLocalVisionProvider()

    return AnthropicVisionProvider()


__all__ = [
    "get_vision_provider",
    "PROVIDER_ENV_VAR",
    "DEFAULT_PROVIDER",
]
