"""
NEXA Africa Operating System
File: core/cognition/providers/openai_transcription_provider.py
Constitutional Owner: Bill Odhiambo Othieno
Description: TranscriptionProvider backed by the real OpenAI Whisper
             API. Consumes the PerceptionEvent produced by
             AudioPerceptionCapturer — never called directly by the
             capturer itself, keeping capture and interpretation as
             separate concerns per the UPL contract.

             Known limitation, stated honestly rather than papered
             over: AudioPerceptionCapturer does not currently capture
             or validate audio format/encoding, so this provider
             assumes a filename/extension the caller supplies (default
             "audio.wav") for Whisper's format detection. If the
             actual audio is a different format, pass the correct
             filename explicitly.
"""

from __future__ import annotations

import io
import os
from typing import Any, Dict, Optional

from core.cognition.providers.base import TranscriptionProvider
from core.perception.events import PerceptionEvent
from core.services.logging.logger import get_logger

logger = get_logger(__name__)

DEFAULT_MODEL_ENV_VAR = "NEXA_TRANSCRIPTION_MODEL"
DEFAULT_MODEL = "whisper-1"
API_KEY_ENV_VAR = "OPENAI_API_KEY"


class OpenAITranscriptionProvider(TranscriptionProvider):
    """
    Wraps the OpenAI Whisper API behind the TranscriptionProvider
    interface.
    """

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

    def transcribe(self, event: PerceptionEvent, filename: str = "audio.wav") -> Dict[str, Any]:
        if not isinstance(event, PerceptionEvent) or event.modality != "audio":
            return {"status": "rejected", "error": "event must be a PerceptionEvent with modality='audio'."}

        audio_bytes = event.payload
        if not isinstance(audio_bytes, (bytes, bytearray)) or len(audio_bytes) == 0:
            return {"status": "rejected", "error": "event.payload must be non-empty bytes."}

        client = self._get_client()
        if client is None:
            logger.warning("OpenAI transcription requested but %s is not configured.", API_KEY_ENV_VAR)
            return {"status": "not_configured", "error": f"{API_KEY_ENV_VAR} is not set."}

        try:
            audio_file = io.BytesIO(bytes(audio_bytes))
            audio_file.name = filename
            response = client.audio.transcriptions.create(model=self._model, file=audio_file)
            text = response.text
            return {"status": "ok", "text": text, "model": self._model, "provider": self.provider_name}
        except Exception as exc:
            logger.exception("OpenAI transcription call failed.")
            return {"status": "error", "error": str(exc)}


__all__ = [
    "OpenAITranscriptionProvider",
    "API_KEY_ENV_VAR",
    "DEFAULT_MODEL",
]
