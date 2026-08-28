"""
NEXA Africa Operating System
File: skills/privileged/image_generation.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Privileged skill for image generation. Goes through
             core/generation/providers/image_router.py instead of
             calling OpenAI directly, so the underlying provider can
             change (including to NEXA's own future local model) without
             this skill changing. Requires IMAGE.GENERATE permission.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry
from core.generation.providers.image_router import get_image_provider

GENERATE_IMAGE_SKILL = SkillManifest(
    skill_id="generation.image",
    name="Generate Image",
    description=(
        "Generates an image from a text prompt via the configured image "
        "provider (OpenAI by default; NEXA_IMAGE_PROVIDER=nexa_local for "
        "NEXA's own future local model). Fails closed if unconfigured."
    ),
    tier="privileged",
    required_permissions=("IMAGE.GENERATE",),
)


def _generate_image_handler(
    prompt: str,
    size: str = "1024x1024",
    provider_name: Optional[str] = None,
) -> Dict[str, Any]:
    provider = get_image_provider(provider_name)
    return provider.generate(prompt, size=size)


def register_privileged_skills(registry: SkillRegistry) -> None:
    registry.register(GENERATE_IMAGE_SKILL, _generate_image_handler)


__all__ = ["GENERATE_IMAGE_SKILL", "register_privileged_skills"]
