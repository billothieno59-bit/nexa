"""
NEXA Africa Operating System
File: core/semantic/parser/voice_command_bridge.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Bridges an audio PerceptionEvent into the same
             UniversalSemanticLayerMapper that text commands already
             use. Voice commands are matched with the same fuzzy/
             intent-based lookup as text (global_usl_mapper's own
             supported_intent_tokens dict) — no separate voice-only
             intent table, so a phrase means the same thing whether
             typed or spoken.

             Transcription failure (not_configured, rejected, error)
             fails closed: no USL token is generated, and
             governed_execution_authorized is never set to True.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from core.cognition.providers.transcription_router import get_transcription_provider
from core.perception.events import PerceptionEvent
from core.semantic.parser.usl_mapper import global_usl_mapper
from core.services.logging.logger import get_logger

logger = get_logger(__name__)


def resolve_voice_command(
    event: PerceptionEvent,
    source_variety: str = "unknown_source",
    filename: str = "audio.wav",
    transcription_provider: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Transcribe an audio PerceptionEvent and resolve it through the
    same USL mapper text commands use.

    Fails closed on any transcription problem — returns a payload with
    governed_execution_authorized=False and does not attempt to guess
    an intent from a partial or failed transcription.
    """
    if not isinstance(event, PerceptionEvent) or event.modality != "audio":
        return {
            "usl_version": "1.0.0",
            "resolved_intent_token": "INTENT_UNKNOWN_PASSTHROUGH",
            "origin_variety_source": source_variety,
            "governed_execution_authorized": False,
            "safety_status": "CLOSED",
            "transcription_status": "rejected",
            "transcription_error": "event must be a PerceptionEvent with modality='audio'.",
        }

    provider = transcription_provider or get_transcription_provider()
    transcription_result = provider.transcribe(event, filename=filename)

    if transcription_result.get("status") != "ok":
        logger.info(
            "Voice command transcription did not succeed: status=%s",
            transcription_result.get("status"),
        )
        return {
            "usl_version": "1.0.0",
            "resolved_intent_token": "INTENT_UNKNOWN_PASSTHROUGH",
            "origin_variety_source": source_variety,
            "governed_execution_authorized": False,
            "safety_status": "CLOSED",
            "transcription_status": transcription_result.get("status"),
            "transcription_error": transcription_result.get("error"),
        }

    transcribed_text = transcription_result.get("text", "")

    usl_result = global_usl_mapper.generate_universal_semantic_token(
        {
            "normalized_swahili_target": transcribed_text,
            "source_variety": source_variety,
        }
    )
    usl_result["transcription_status"] = "ok"
    usl_result["transcribed_text"] = transcribed_text
    return usl_result


__all__ = [
    "resolve_voice_command",
]