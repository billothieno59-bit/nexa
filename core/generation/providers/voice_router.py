"""
NEXA Africa Operating System
File: core/generation/providers/voice_router.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Selects a VoiceGenerationProvider by configuration.
             Defaults to ElevenLabs today; NEXA_VOICE_PROVIDER=nexa_local
             reserves the seam for a future funded local model.
"""

from __future__ import annotations

import os
from typing import Optional

from core.generation.providers.base import VoiceGenerationProvider
from core.generation.providers.elevenlabs_voice_provider import ElevenLabsVoiceProvider
from core.generation.providers.local_voice_provider import NexaLocalVoiceProvider

PROVIDER_ENV_VAR = "NEXA_VOICE_PROVIDER"
DEFAULT_PROVIDER = "elevenlabs"


def get_voice_provider(name: Optional[str] = None) -> VoiceGenerationProvider:
    selected = name or os.environ.get(PROVIDER_ENV_VAR, DEFAULT_PROVIDER)

    if selected == "nexa_local":
        return NexaLocalVoiceProvider()

    return ElevenLabsVoiceProvider()


__all__ = ["get_voice_provider", "PROVIDER_ENV_VAR", "DEFAULT_PROVIDER"]
