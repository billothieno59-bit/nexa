"""
NEXA Africa Operating System
File: skills/builtin/accessibility_screen_reader.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Builtin skill wrapping the screen-reader-friendly formatter.
"""

from __future__ import annotations

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry
from core.interaction.accessibility.screen_reader_formatter import (
    format_for_screen_reader,
)

FORMAT_SCREEN_READER_SKILL = SkillManifest(
    skill_id="accessibility.format_screen_reader",
    name="Format for Screen Reader",
    description="Expands abbreviations and strips decorative characters for screen readers.",
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)


def register_builtin_skills(registry: SkillRegistry) -> None:
    registry.register(FORMAT_SCREEN_READER_SKILL, format_for_screen_reader)


__all__ = [
    "FORMAT_SCREEN_READER_SKILL",
    "register_builtin_skills",
]
