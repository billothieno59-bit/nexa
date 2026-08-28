"""
NEXA Canonical Handler Registry Bootstrap.

This module exposes the single canonical HandlerRegistry used by the
execution layer. Every component should obtain the registry from here
instead of creating its own registry instance.

In addition to the built-in diagnostic/resource handlers, every
registered skill (from skills/registry/bootstrap.py) is also wrapped as
an ExecutionActionHandler here, so skills are reachable through the main
governed execution pipeline using their skill_id as the action name.
"""

from __future__ import annotations

from core.execution.executor.registry import HandlerRegistry
from core.execution.executor.action_handlers import (
    DiagnosticCheckHandler,
    ResourceTransactionHandler,
)
import skills.registry.bootstrap as _skills_bootstrap  # populates global_skill_registry
from skills.registry.execution_handler_adapter import build_skill_action_handlers


_CANONICAL_REGISTRY = HandlerRegistry(
    handlers=(
        DiagnosticCheckHandler(),
        ResourceTransactionHandler(),
    )
    + build_skill_action_handlers(_skills_bootstrap.global_skill_registry),
)


def get_handler_registry() -> HandlerRegistry:
    """
    Return the canonical immutable handler registry.

    The same registry instance is shared throughout the execution layer.
    """
    return _CANONICAL_REGISTRY


__all__ = [
    "get_handler_registry",
]
