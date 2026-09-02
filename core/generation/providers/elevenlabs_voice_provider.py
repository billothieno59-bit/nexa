"""
NEXA Africa Operating System
File: core/generation/providers/elevenlabs_voice_provider.py
Constitutional Owner: Bill Odhiambo Othieno
Description: VoiceGenerationProvider backed by the real ElevenLabs API.
             Same logic previously inline in
             skills/privileged/voice_generation.py, now behind the
             VoiceGenerationProvider interface.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from core.generation.providers.base import VoiceGenerationProvider
from core.services.logging.logger import get_logger

logger = get_logger(__name__)

DEFAULT_VOICE_ENV_VAR = "NEXA_VOICE_ID"
DEFAULT_VOICE_ID = "default"
API_KEY_ENV_VAR = "ELEVENLABS_API_KEY"


class ElevenLabsVoiceProvider(VoiceGenerationProvider):
    def __init__(self, client: Optional[Any] = None, voice_id: Optional[str] = None) -> None:
        self._injected_client = client
        self._voice_id = voice_id or os.environ.get(DEFAULT_VOICE_ENV_VAR, DEFAULT_VOICE_ID)

    @property
    def provider_name(self) -> str:
        return "elevenlabs"

    def _get_client(self) -> Optional[Any]:
        if self._injected_client is not None:
            return self._injected_client
        api_key = os.environ.get(API_KEY_ENV_VAR)
        if not api_key:
            return None
        from elevenlabs.client import ElevenLabs  # imported lazily

        return ElevenLabs(api_key=api_key)

    def generate(self, text: str) -> Dict[str, Any]:
        if not isinstance(text, str) or not text.strip():
            return {"status": "rejected", "error": "text must be a non-empty string."}

        client = self._get_client()
        if client is None:
            logger.warning("ElevenLabs voice generation requested but %s is not configured.", API_KEY_ENV_VAR)
            return {"status": "not_configured", "error": f"{API_KEY_ENV_VAR} is not set."}

        try:
            audio_bytes = client.generate(text=text, voice=self._voice_id)
            if isinstance(audio_bytes, (bytes, bytearray)):
                audio_length = len(audio_bytes)
            else:
                audio_length = len(b"".join(audio_bytes))
            return {
                "status": "ok",
                "audio_bytes_length": audio_length,
                "voice_id": self._voice_id,
                "provider": self.provider_name,
            }
        except Exception as exc:
            logger.exception("ElevenLabs voice generation call failed.")
            return {"status": "error", "error": str(exc)}


__all__ = ["ElevenLabsVoiceProvider", "API_KEY_ENV_VAR", "DEFAULT_VOICE_ID"]
