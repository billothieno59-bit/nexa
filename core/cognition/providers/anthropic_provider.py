"""
NEXA Africa Operating System
File: core/cognition/providers/anthropic_provider.py
Constitutional Owner: Bill Odhiambo Othieno
Description: ReasoningProvider backed by the real Anthropic Claude API.
             This is the same logic previously inline in
             skills/privileged/ai_reasoning.py, now behind the
             ReasoningProvider interface so it can be swapped for
             another provider (including a future NEXA-owned model)
             without changing the calling skill.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from core.cognition.providers.base import ReasoningProvider
from core.services.logging.logger import get_logger

logger = get_logger(__name__)

DEFAULT_MODEL_ENV_VAR = "NEXA_LLM_MODEL"
DEFAULT_MODEL = "claude-sonnet-5"
API_KEY_ENV_VAR = "ANTHROPIC_API_KEY"


class AnthropicReasoningProvider(ReasoningProvider):
    """
    Wraps the Anthropic Claude API behind the ReasoningProvider interface.
    """

    def __init__(self, client: Optional[Any] = None, model: Optional[str] = None) -> None:
        self._injected_client = client
        self._model = model or os.environ.get(DEFAULT_MODEL_ENV_VAR, DEFAULT_MODEL)

    @property
    def provider_name(self) -> str:
        return "anthropic"

    def _get_client(self) -> Optional[Any]:
        if self._injected_client is not None:
            return self._injected_client

        api_key = os.environ.get(API_KEY_ENV_VAR)
        if not api_key:
            return None

        import anthropic  # imported lazily

        return anthropic.Anthropic(api_key=api_key)

    def reason(self, prompt: str, max_tokens: int = 1024) -> Dict[str, Any]:
        if not isinstance(prompt, str) or not prompt.strip():
            return {"status": "rejected", "error": "prompt must be a non-empty string."}

        client = self._get_client()
        if client is None:
            logger.warning("Anthropic reasoning requested but %s is not configured.", API_KEY_ENV_VAR)
            return {
                "status": "not_configured",
                "error": f"{API_KEY_ENV_VAR} is not set.",
            }

        try:
            response = client.messages.create(
                model=self._model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            text = response.content[0].text
            return {"status": "ok", "response": text, "model": self._model, "provider": self.provider_name}
        except Exception as exc:
            logger.exception("Anthropic reasoning call failed.")
            return {"status": "error", "error": str(exc)}


__all__ = [
    "AnthropicReasoningProvider",
    "API_KEY_ENV_VAR",
    "DEFAULT_MODEL",
]
