"""
NEXA Execution Dispatcher.

The Execution Dispatcher receives an OrchestrationResult and determines
whether the proposed execution steps may be handed to a future executor.

Architectural boundary:

    Decision Engine
          |
          v
    Execution Planner
          |
          v
    ExecutionPlan
          |
          v
    Execution Orchestrator
          |
          v
    OrchestrationResult
          |
          v
    Execution Dispatcher
          |
          v
    Future Executor

This module does NOT execute real-world actions.

It must not:

    - call external services
    - control devices
    - modify files
    - perform network operations
    - create external side effects
    - bypass confirmation requirements
    - bypass governance

The dispatcher only determines what is eligible to proceed
to the future execution layer.
"""

from __future__ import annotations

from dataclasses import dataclass

from core.execution.orchestrator.orchestrator import OrchestrationResult
from core.execution.orchestrator.planner.planner import PlanStep


@dataclass(frozen=True)
class DispatchResult:
    """
    Represents the result of dispatching an orchestration result.

    This object does not represent successful execution of an action.

    It only describes whether the proposed steps are eligible to be
    handed to a future executor.
    """

    status: str
    intent: str
    steps: tuple[PlanStep, ...] = ()
    reason: str = ""


class ExecutionDispatcher:
    """
    Safely dispatch an OrchestrationResult toward the future executor.

    The dispatcher does not execute actions.

    It acts as the final boundary before the future execution layer.
    """

    def dispatch(
        self,
        result: OrchestrationResult,
    ) -> DispatchResult:
        """
        Dispatch an OrchestrationResult.

        Parameters
        ----------
        result:
            An OrchestrationResult produced by the Execution Orchestrator.

        Returns
        -------
        DispatchResult
            A structured result describing whether the proposed steps
            may proceed to the future execution layer.
        """

        if result.status == "blocked":
            return DispatchResult(
                status="blocked",
                intent=result.intent,
                steps=(),
                reason=result.reason,
            )

        if result.status == "awaiting_confirmation":
            return DispatchResult(
                status="awaiting_confirmation",
                intent=result.intent,
                steps=(),
                reason="Execution requires confirmation.",
            )

        if result.status == "ready":
            return DispatchResult(
                status="ready_for_execution",
                intent=result.intent,
                steps=result.steps,
                reason=result.reason,
            )

        return DispatchResult(
            status="blocked",
            intent=result.intent,
            steps=(),
            reason="Unknown orchestration result status.",
        )


__all__ = [
    "DispatchResult",
    "ExecutionDispatcher",
]
