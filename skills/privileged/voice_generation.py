"""
NEXA Africa Operating System
File: skills/privileged/voice_generation.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Privileged skill for voice generation. Goes through
             core/generation/providers/voice_router.py instead of
             calling ElevenLabs directly, so the underlying provider can
             change (including to NEXA's own future local model) without
             this skill changing. Requires VOICE.GENERATE permission.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry
from core.generation.providers.voice_router import get_voice_provider

GENERATE_VOICE_SKILL = SkillManifest(
    skill_id="generation.voice",
    name="Generate Voice",
    description=(
        "Synthesizes speech audio from text via the configured voice "
        "provider (ElevenLabs by default; NEXA_VOICE_PROVIDER=nexa_local "
        "for NEXA's own future local model). Fails closed if unconfigured."
    ),
    tier="privileged",
    required_permissions=("VOICE.GENERATE",),
)


def _generate_voice_handler(text: str, provider_name: Optional[str] = None) -> Dict[str, Any]:
    provider = get_voice_provider(provider_name)
    return provider.generate(text)


def register_privileged_skills(registry: SkillRegistry) -> None:
    registry.register(GENERATE_VOICE_SKILL, _generate_voice_handler)


__all__ = ["GENERATE_VOICE_SKILL", "register_privileged_skills"]
