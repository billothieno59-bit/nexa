"""
NEXA Africa Operating System
File: skills/builtin/accessibility_simplify.py
Constitutional Owner: Bill Odhiambo Othieno
Description: First real builtin skill. Wraps the existing, tested
             accessibility text simplifier as a registered skill.
"""

from __future__ import annotations

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry
from core.interaction.accessibility.text_simplifier import simplify_for_accessibility

SIMPLIFY_TEXT_SKILL = SkillManifest(
    skill_id="accessibility.simplify_text",
    name="Simplify Text",
    description="Breaks long sentences into shorter ones for accessibility.",
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)


def register_builtin_skills(registry: SkillRegistry) -> None:
    """
    Register all builtin skills into the given registry.
    """
    registry.register(SIMPLIFY_TEXT_SKILL, simplify_for_accessibility)


__all__ = [
    "SIMPLIFY_TEXT_SKILL",
    "register_builtin_skills",
]
