"""
NEXA Africa Operating System
File: core/cognition/providers/router.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Selects a ReasoningProvider by configuration. Defaults to
             the real Anthropic provider today; switching NEXA_AI_PROVIDER
             to "nexa_local" uses NEXA's own local provider instead, with
             no code changes to any caller (like the ai.reason skill).
             This is the seam a future NEXA-owned model plugs into.
"""

from __future__ import annotations

import os
from typing import Optional

from core.cognition.providers.base import ReasoningProvider
from core.cognition.providers.anthropic_provider import AnthropicReasoningProvider
from core.cognition.providers.local_provider import NexaLocalProvider

PROVIDER_ENV_VAR = "NEXA_AI_PROVIDER"
DEFAULT_PROVIDER = "anthropic"


def get_reasoning_provider(name: Optional[str] = None) -> ReasoningProvider:
    """
    Return the configured ReasoningProvider. Unknown names fail closed
    by falling back to the default rather than silently returning None.
    """
    selected = name or os.environ.get(PROVIDER_ENV_VAR, DEFAULT_PROVIDER)

    if selected == "nexa_local":
        return NexaLocalProvider()

    if selected == "anthropic":
        return AnthropicReasoningProvider()

    return AnthropicReasoningProvider()


__all__ = [
    "get_reasoning_provider",
    "PROVIDER_ENV_VAR",
    "DEFAULT_PROVIDER",
]
