"""
NEXA Africa Operating System
File: skills/builtin/perception_capture.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Builtin skill wrapping the existing, tested text perception
             capturer.
"""

from __future__ import annotations

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry
from core.perception.capture.text_capturer import TextPerceptionCapturer

CAPTURE_TEXT_SKILL = SkillManifest(
    skill_id="perception.capture_text",
    name="Capture Text",
    description="Structures raw text input into a PerceptionEvent.",
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)

_capturer = TextPerceptionCapturer()


def _capture_text_handler(raw_input: str, source: str = "skill_invocation"):
    return _capturer.capture(raw_input, source=source)


def register_builtin_skills(registry: SkillRegistry) -> None:
    registry.register(CAPTURE_TEXT_SKILL, _capture_text_handler)


__all__ = [
    "CAPTURE_TEXT_SKILL",
    "register_builtin_skills",
]
