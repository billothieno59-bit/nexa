"""
NEXA Africa Operating System
File: core/cognition/providers/base.py
Constitutional Owner: Bill Odhiambo Othieno
Description: ReasoningProvider — the abstraction every reasoning backend
             implements, whether an external API (Anthropic) or a future
             model NEXA trains and owns itself. Callers (like the
             ai.reason skill) depend on this interface, never on a
             specific vendor, so switching providers never requires
             rewriting the skill that uses them.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from core.perception.events import PerceptionEvent


class ReasoningProvider(ABC):
    """
    Common interface for anything that can answer an open-ended prompt.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Short identifier for this provider (e.g. 'anthropic', 'nexa_local')."""
        raise NotImplementedError

    @abstractmethod
    def reason(self, prompt: str, max_tokens: int = 1024) -> Dict[str, Any]:
        """
        Answer prompt. Must return a dict with at least a "status" key
        ("ok", "not_configured", "rejected", or "error"), following the
        same fail-closed contract already used throughout this codebase.
        """
        raise NotImplementedError


class TranscriptionProvider(ABC):
    """
    Common interface for anything that can turn a captured audio
    PerceptionEvent into text. Consumes what
    core.perception.capture.audio_capturer.AudioPerceptionCapturer
    produces — the capturer itself never transcribes, per the UPL
    contract.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Short identifier for this provider (e.g. 'openai', 'nexa_local')."""
        raise NotImplementedError

    @abstractmethod
    def transcribe(self, event: PerceptionEvent) -> Dict[str, Any]:
        """
        Transcribe an audio PerceptionEvent. Must return a dict with at
        least a "status" key ("ok", "not_configured", "not_implemented",
        "rejected", or "error"), following the same fail-closed contract
        used throughout this codebase. On "ok", must include "text".
        """
        raise NotImplementedError


class VisionUnderstandingProvider(ABC):
    """
    Common interface for anything that can describe or answer questions
    about a captured image PerceptionEvent. Consumes what
    core.perception.capture.image_capturer.ImagePerceptionCapturer
    produces — the capturer itself never interprets, per the UPL
    contract.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Short identifier for this provider (e.g. 'anthropic', 'nexa_local')."""
        raise NotImplementedError

    @abstractmethod
    def describe(self, event: PerceptionEvent, prompt: str = "Describe this image.") -> Dict[str, Any]:
        """
        Describe or answer a question about an image PerceptionEvent.
        Must return a dict with at least a "status" key ("ok",
        "not_configured", "not_implemented", "rejected", or "error").
        On "ok", must include "response".
        """
        raise NotImplementedError


__all__ = [
    "ReasoningProvider",
    "TranscriptionProvider",
    "VisionUnderstandingProvider",
]
