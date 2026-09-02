"""
NEXA African Operating System
Execution Planner

Canonical Universal:
    UOL — Universal Orchestration Layer

Purpose:
    Convert a validated cognitive Decision into a structured
    execution plan without performing execution.

Architectural boundary:

    UCL
      |
      v
    USL
      |
      v
    Cognition
      |
      v
    Decision
      |
      v
    UOL Planner
      |
      v
    ExecutionPlan
      |
      v
    Future Execution Orchestrator

This module does NOT execute actions.

The planner must not:

    - call external services
    - perform network operations
    - control devices
    - modify files
    - perform shell commands
    - bypass governance
    - bypass confirmation requirements
    - create external side effects

Those responsibilities belong to later execution components
under the appropriate constitutional boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from core.cognition.thinking.decision_engine import Decision


@dataclass(frozen=True)
class PlanStep:
    """
    Represents one proposed step in an execution plan.

    A PlanStep describes what a future executor may perform.
    It does not perform the action itself.
    """

    action: str
    parameters: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ExecutionPlan:
    """
    Represents a structured execution plan.

    The plan is descriptive only. Creating an ExecutionPlan
    must never create an external side effect.
    """

    status: str
    intent: str
    requires_confirmation: bool
    steps: tuple[PlanStep, ...] = ()
    reason: str = ""


class ExecutionPlanner:
    """
    Convert a cognitive Decision into a safe ExecutionPlan.

    The planner is intentionally conservative.

    Any decision requiring confirmation remains in an
    awaiting_confirmation state.

    The planner does not authorize execution. It only
    represents the decision in a form that a future
    execution orchestrator can consume.
    """

    def create_plan(self, decision: Decision) -> ExecutionPlan:
        """
        Create an execution plan from a cognitive Decision.

        Parameters
        ----------
        decision:
            A Decision produced by the canonical cognition layer.

        Returns
        -------
        ExecutionPlan
            A structured, non-executing execution plan.
        """

        if decision.decision_type == "blocked":
            return ExecutionPlan(
                status="blocked",
                intent=decision.intent,
                requires_confirmation=False,
                steps=(),
                reason=decision.reason,
            )

        if decision.decision_type == "informational":
            return ExecutionPlan(
                status="ready",
                intent=decision.intent,
                requires_confirmation=False,
                steps=(
                    PlanStep(
                        action="respond",
                        parameters={
                            "intent": decision.intent,
                        },
                    ),
                ),
                reason=decision.reason,
            )

        if decision.decision_type == "confirmation_required":
            return ExecutionPlan(
                status="awaiting_confirmation",
                intent=decision.intent,
                requires_confirmation=True,
                steps=(
                    PlanStep(
                        action="await_confirmation",
                        parameters={
                            "intent": decision.intent,
                        },
                    ),
                ),
                reason=decision.reason,
            )

        return ExecutionPlan(
            status="blocked",
            intent=decision.intent,
            requires_confirmation=False,
            steps=(),
            reason="Unknown decision type.",
        )


__all__ = [
    "PlanStep",
    "ExecutionPlan",
    "ExecutionPlanner",
]
