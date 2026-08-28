"""
NEXA Africa Operating System
File: core/cognition/providers/transcription_router.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Selects a TranscriptionProvider by configuration. Defaults
             to the real OpenAI Whisper provider today; switching
             NEXA_TRANSCRIPTION_PROVIDER to "nexa_local" reserves the
             seam for a future funded local model, with no code changes
             to any caller.
"""

from __future__ import annotations

import os
from typing import Optional

from core.cognition.providers.base import TranscriptionProvider
from core.cognition.providers.openai_transcription_provider import OpenAITranscriptionProvider
from core.cognition.providers.local_transcription_provider import NexaLocalTranscriptionProvider

PROVIDER_ENV_VAR = "NEXA_TRANSCRIPTION_PROVIDER"
DEFAULT_PROVIDER = "openai"


def get_transcription_provider(name: Optional[str] = None) -> TranscriptionProvider:
    """
    Return the configured TranscriptionProvider. Unknown names fail
    closed by falling back to the default rather than silently
    returning None.
    """
    selected = name or os.environ.get(PROVIDER_ENV_VAR, DEFAULT_PROVIDER)

    if selected == "nexa_local":
        return NexaLocalTranscriptionProvider()

    return OpenAITranscriptionProvider()


__all__ = [
    "get_transcription_provider",
    "PROVIDER_ENV_VAR",
    "DEFAULT_PROVIDER",
]
