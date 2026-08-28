"""
NEXA Africa Operating System
File: core/generation/providers/base.py
Constitutional Owner: Bill Odhiambo Othieno
Description: ImageGenerationProvider and VoiceGenerationProvider — the
             abstractions every image/voice backend implements, whether
             a third-party API (OpenAI, ElevenLabs) or a future model
             NEXA trains and owns itself. Skills depend on these
             interfaces, never on a specific vendor, so a funded local
             model can be plugged in later without rewriting any skill.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class ImageGenerationProvider(ABC):
    """Common interface for anything that can generate an image from a prompt."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate(self, prompt: str, size: str = "1024x1024") -> Dict[str, Any]:
        """
        Must return a dict with at least "status" ("ok", "not_configured",
        "not_implemented", "rejected", or "error"), following the same
        fail-closed contract used throughout this codebase.
        """
        raise NotImplementedError


class VoiceGenerationProvider(ABC):
    """Common interface for anything that can synthesize speech from text."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate(self, text: str) -> Dict[str, Any]:
        """
        Must return a dict with at least "status" ("ok", "not_configured",
        "not_implemented", "rejected", or "error").
        """
        raise NotImplementedError


__all__ = [
    "ImageGenerationProvider",
    "VoiceGenerationProvider",
]
