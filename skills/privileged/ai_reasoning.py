"""
NEXA Africa Operating System
File: skills/privileged/ai_reasoning.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Privileged skill for open-ended reasoning. Goes through
             core/cognition/providers/router.py instead of calling any
             AI vendor directly, so the underlying provider (Anthropic
             today, NEXA's own local model in the future) can change
             without this skill changing. Requires AI.REASON permission.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry
from core.cognition.providers.router import get_reasoning_provider

AI_REASON_SKILL = SkillManifest(
    skill_id="ai.reason",
    name="AI Reasoning",
    description=(
        "Answers an open-ended prompt via the configured reasoning provider "
        "(Anthropic by default; NEXA_AI_PROVIDER=nexa_local for NEXA's own "
        "local provider). Fails closed rather than fabricating a response."
    ),
    tier="privileged",
    required_permissions=("AI.REASON",),
)


def _reason_handler(prompt: str, max_tokens: int = 1024, provider_name: Optional[str] = None) -> Dict[str, Any]:
    provider = get_reasoning_provider(provider_name)
    return provider.reason(prompt, max_tokens=max_tokens)


def register_privileged_skills(registry: SkillRegistry) -> None:
    registry.register(AI_REASON_SKILL, _reason_handler)


__all__ = [
    "AI_REASON_SKILL",
    "register_privileged_skills",
]
