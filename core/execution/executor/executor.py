"""
NEXA Execution Layer.

The executor is the architectural boundary between:

    Execution Orchestrator
            |
            v
       ExecutionPlan
            |
            v
          Executor
            |
            v
     Handler Registry
            |
            v
       Action Handlers

IMPORTANT
---------
The executor:

- accepts an ExecutionPlan
- validates whether execution is allowed
- refuses blocked plans
- refuses plans awaiting confirmation
- for ready plans, resolves registered handlers and invokes them
- if no handler is registered for a step's action, that step is
  accepted with no side effect (this is the default for most
  informational responses, which have no registered handler)
- does NOT access the network, modify files, control devices, or
  invoke operating-system commands itself — those behaviors only
  exist if a registered handler's own implementation performs them,
  and today's registered handlers are side-effect-free placeholders
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict

from core.execution.executor.handler import ExecutionActionHandler
from core.execution.executor.registry import HandlerRegistry
from core.execution.executor.bootstrap import get_handler_registry
from core.execution.orchestrator.planner.planner import (
    ExecutionPlan,
    PlanStep,
)
from core.services.logging.logger import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class ExecutionResult:
    """
    Result produced by the execution layer.
    """

    status: str
    plan: ExecutionPlan
    executed_steps: tuple[PlanStep, ...] = ()
    message: str = ""
    handler_results: Dict[str, Any] = field(default_factory=dict)


class ExecutionExecutor:
    """
    Execution boundary for NEXA.

    Ready plans have their steps' handlers resolved from the
    registry. If a handler is registered for a step's action, it is
    invoked. If no handler is registered, the step is accepted
    without any side effect.
    """

    def __init__(
        self,
        registry: HandlerRegistry | None = None,
    ) -> None:
        """
        Create an execution executor.

        Parameters
        ----------
        registry:
            Optional controlled handler registry.

            When omitted, the canonical registry from bootstrap.py is
            used, so the executor sees the same registered handlers as
            every other component by default.
        """

        self.registry = registry if registry is not None else get_handler_registry()

    def _resolve_handlers(
        self,
        plan: ExecutionPlan,
    ) -> tuple[ExecutionActionHandler | None, ...]:
        """
        Resolve registered handlers for the plan steps.

        A missing handler is not an error — most plan steps
        (e.g. informational responses) have no registered handler
        and are accepted without invocation.
        """

        resolved: list[ExecutionActionHandler | None] = []

        for step in plan.steps:
            resolved.append(
                self.registry.get_handler(step.action)
            )

        return tuple(resolved)

    def execute(self, plan: ExecutionPlan) -> ExecutionResult:
        """
        Process an execution plan.

        Rules
        -----
        blocked
            Never execute.

        awaiting_confirmation
            Never execute.

        ready
            Resolve registered handlers. Invoke any handler that
            is found. Steps with no registered handler are accepted
            with no side effect.

        unknown status
            Fail closed.
        """

        if not isinstance(plan, ExecutionPlan):
            raise TypeError(
                "ExecutionExecutor.execute() requires an ExecutionPlan."
            )

        if plan.status == "blocked":
            logger.info(
                "Execution plan blocked. intent=%s reason=%s",
                plan.intent,
                plan.reason,
            )
            return ExecutionResult(
                status="blocked",
                plan=plan,
                executed_steps=(),
                message="Execution plan is blocked.",
            )

        if plan.status == "awaiting_confirmation":
            logger.info(
                "Execution plan awaiting confirmation. intent=%s",
                plan.intent,
            )
            return ExecutionResult(
                status="awaiting_confirmation",
                plan=plan,
                executed_steps=(),
                message="Execution requires confirmation.",
            )

        if plan.status == "ready":
            handlers = self._resolve_handlers(plan)

            executed: list[PlanStep] = []
            handler_results: Dict[str, Any] = {}

            for step, handler in zip(plan.steps, handlers):
                if handler is not None:
                    logger.info(
                        "Invoking handler for action=%s", step.action
                    )
                    outcome = handler.handle(step)
                    executed.append(step)
                    handler_results[step.action] = outcome

            if executed:
                logger.info(
                    "Execution plan executed. intent=%s actions=%s",
                    plan.intent,
                    [s.action for s in executed],
                )
                return ExecutionResult(
                    status="executed",
                    plan=plan,
                    executed_steps=tuple(executed),
                    message=(
                        "Execution plan executed via registered handlers."
                    ),
                    handler_results=handler_results,
                )

            logger.info(
                "Execution plan accepted with no registered handler. intent=%s",
                plan.intent,
            )
            return ExecutionResult(
                status="accepted",
                plan=plan,
                executed_steps=(),
                message=(
                    "Execution plan accepted. "
                    "No external action was performed."
                ),
            )

        logger.warning(
            "Unknown execution plan status '%s'. Failing closed. intent=%s",
            plan.status,
            plan.intent,
        )
        return ExecutionResult(
            status="blocked",
            plan=plan,
            executed_steps=(),
            message="Unknown execution state. Failing closed.",
        )


__all__ = [
    "ExecutionExecutor",
    "ExecutionResult",
]
