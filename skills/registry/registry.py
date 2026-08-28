"""
NEXA Africa Operating System
File: skills/registry/registry.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Stores SkillManifests and their handler callables, keyed by
             skill_id, per core/contracts/skills/skills_contract_v1.md.
             This registry never invokes a handler and never authorizes
             anything.
"""

from __future__ import annotations

from typing import Callable, Dict, Optional, Tuple

from skills.registry.manifest import SkillManifest
from core.services.logging.logger import get_logger

logger = get_logger(__name__)


class DuplicateSkillError(Exception):
    """Raised when registering a skill_id that is already registered."""


class SkillRegistry:
    """
    Registers skill manifests and their handlers.

    This registry is a directory only. It does not execute handlers and
    does not authorize anything — that remains the responsibility of the
    governed execution pipeline and authorization policy.
    """

    def __init__(self) -> None:
        self._manifests: Dict[str, SkillManifest] = {}
        self._handlers: Dict[str, Callable[..., object]] = {}

    def register(self, manifest: SkillManifest, handler: Callable[..., object]) -> None:
        if not isinstance(manifest, SkillManifest):
            raise TypeError("SkillRegistry.register() requires a SkillManifest.")

        if manifest.skill_id in self._manifests:
            raise DuplicateSkillError(
                f"Skill '{manifest.skill_id}' is already registered."
            )

        if not callable(handler):
            raise TypeError("SkillRegistry.register() requires a callable handler.")

        self._manifests[manifest.skill_id] = manifest
        self._handlers[manifest.skill_id] = handler
        logger.info(
            "Registered skill id=%s tier=%s required_permissions=%s",
            manifest.skill_id,
            manifest.tier,
            manifest.required_permissions,
        )

    def get_manifest(self, skill_id: str) -> Optional[SkillManifest]:
        return self._manifests.get(skill_id)

    def get_handler(self, skill_id: str) -> Optional[Callable[..., object]]:
        return self._handlers.get(skill_id)

    def list_skill_ids(self) -> Tuple[str, ...]:
        return tuple(self._manifests.keys())

    def required_permissions_for(self, skill_id: str) -> Tuple[str, ...]:
        manifest = self._manifests.get(skill_id)
        if manifest is None:
            return ()
        return manifest.required_permissions


global_skill_registry = SkillRegistry()


__all__ = [
    "SkillRegistry",
    "DuplicateSkillError",
    "global_skill_registry",
]
