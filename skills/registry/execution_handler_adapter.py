"""
NEXA Africa Operating System
File: skills/registry/execution_handler_adapter.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Wraps skills as ExecutionActionHandler instances so they can
             be reached through the main governed execution pipeline
             (Decision -> Planner -> Orchestrator -> Dispatcher ->
             Authorization -> Executor), not only via a direct call to
             execution_bridge.invoke_skill(). Each skill's skill_id
             becomes its action_name in the canonical HandlerRegistry.
             Invocation still goes through invoke_skill() underneath, so
             identity/trust resolution and SkillAuthorizationGate
             enforcement are never bypassed by reaching a skill this way.
"""

from __future__ import annotations

from typing import Tuple

from core.execution.executor.handler import ExecutionActionHandler
from core.execution.orchestrator.planner.planner import PlanStep
from skills.registry.registry import SkillRegistry, global_skill_registry
from skills.registry.execution_bridge import invoke_skill


class SkillActionHandler(ExecutionActionHandler):
    """
    Adapts a single registered skill into an ExecutionActionHandler.
    """

    def __init__(self, skill_id: str, registry: SkillRegistry) -> None:
        self._skill_id = skill_id
        self._registry = registry

    @property
    def action_name(self) -> str:
        return self._skill_id

    def handle(self, step: PlanStep):
        params = dict(step.parameters or {})
        caller_id = params.pop("caller_id", "anonymous")
        requested_intent = params.pop("requested_intent", "GENERAL.QUERY")

        return invoke_skill(
            caller_id=caller_id,
            skill_id=self._skill_id,
            requested_intent=requested_intent,
            registry=self._registry,
            **params,
        )


def build_skill_action_handlers(
    registry: SkillRegistry = global_skill_registry,
) -> Tuple[SkillActionHandler, ...]:
    """
    Build one SkillActionHandler per skill currently registered in
    `registry`, so every skill becomes reachable as an action in the
    canonical execution HandlerRegistry.
    """
    return tuple(SkillActionHandler(skill_id, registry) for skill_id in registry.list_skill_ids())


__all__ = [
    "SkillActionHandler",
    "build_skill_action_handlers",
]
