"""
NEXA Execution Pipeline.

The Execution Pipeline connects the execution layers in order:

    Decision
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
    DispatchResult
        |
        v
    Authorization Policy
        |
        v
    AuthorizationResult
        |
        v
    Execution Executor
        |
        v
    ExecutionResult

The pipeline coordinates these components without bypassing
their individual safety boundaries.

The authorization policy is the controlled gate between
dispatch and execution.

The executor remains dry-run only.
"""

from __future__ import annotations

from dataclasses import dataclass

from core.cognition.thinking.decision_engine import Decision

from core.execution.authorization.policy import (
    AuthorizationResult,
    ExecutionAuthorizationPolicy,
)

from core.execution.orchestrator.planner.planner import (
    ExecutionPlan,
    ExecutionPlanner,
)

from core.execution.orchestrator.orchestrator import (
    ExecutionOrchestrator,
    OrchestrationResult,
)

from core.execution.dispatcher.dispatcher import (
    ExecutionDispatcher,
    DispatchResult,
)

from core.execution.executor.executor import (
    ExecutionExecutor,
    ExecutionResult,
)


@dataclass(frozen=True)
class ExecutionPipelineResult:
    """
    Complete result produced by the execution pipeline.

    This object contains the result of every execution boundary.
    """

    plan: ExecutionPlan
    orchestration: OrchestrationResult
    dispatch: DispatchResult
    authorization: AuthorizationResult
    execution: ExecutionResult


class ExecutionPipeline:
    """
    Coordinate the complete NEXA execution pipeline.

    The pipeline does not bypass:

    - governance
    - confirmation
    - orchestration
    - dispatch
    - authorization
    - executor safety checks
    """

    def __init__(
        self,
        planner: ExecutionPlanner | None = None,
        orchestrator: ExecutionOrchestrator | None = None,
        dispatcher: ExecutionDispatcher | None = None,
        authorization_policy: ExecutionAuthorizationPolicy | None = None,
        executor: ExecutionExecutor | None = None,
    ) -> None:
        self.planner = planner or ExecutionPlanner()
        self.orchestrator = orchestrator or ExecutionOrchestrator()
        self.dispatcher = dispatcher or ExecutionDispatcher()

        self.authorization_policy = (
            authorization_policy
            or ExecutionAuthorizationPolicy(
                allowed_actions=("respond",),
            )
        )

        self.executor = executor or ExecutionExecutor()

    def process(self, decision: Decision) -> ExecutionPipelineResult:
        """
        Process a Decision through the complete execution pipeline.

        Execution sequence:

            Decision
                ↓
            Planner
                ↓
            ExecutionPlan
                ↓
            Orchestrator
                ↓
            Dispatcher
                ↓
            Authorization
                ↓
            Executor
        """

        if not isinstance(decision, Decision):
            raise TypeError(
                "ExecutionPipeline.process() requires a Decision."
            )

        plan = self.planner.create_plan(decision)

        orchestration = self.orchestrator.orchestrate(plan)

        plan = orchestration.plan

        dispatch = self.dispatcher.dispatch(orchestration)

        if dispatch.status == "blocked":
            authorization = AuthorizationResult(
                status="denied",
                plan=plan,
                message=dispatch.reason or "Execution was blocked.",
            )

            execution = ExecutionResult(
                status="blocked",
                plan=plan,
                executed_steps=(),
                message=dispatch.reason or "Execution was blocked.",
            )

            return ExecutionPipelineResult(
                plan=plan,
                orchestration=orchestration,
                dispatch=dispatch,
                authorization=authorization,
                execution=execution,
            )

        if dispatch.status == "awaiting_confirmation":
            authorization = AuthorizationResult(
                status="denied",
                plan=plan,
                message="Execution requires confirmation.",
            )

            execution = ExecutionResult(
                status="awaiting_confirmation",
                plan=plan,
                executed_steps=(),
                message="Execution requires confirmation.",
            )

            return ExecutionPipelineResult(
                plan=plan,
                orchestration=orchestration,
                dispatch=dispatch,
                authorization=authorization,
                execution=execution,
            )

        if dispatch.status != "ready_for_execution":
            authorization = AuthorizationResult(
                status="denied",
                plan=plan,
                message="Unknown dispatch state. Failing closed.",
            )

            execution = ExecutionResult(
                status="blocked",
                plan=plan,
                executed_steps=(),
                message="Unknown dispatch state. Failing closed.",
            )

            return ExecutionPipelineResult(
                plan=plan,
                orchestration=orchestration,
                dispatch=dispatch,
                authorization=authorization,
                execution=execution,
            )

        authorization = self.authorization_policy.authorize(plan)

        if authorization.status != "authorized":
            execution = ExecutionResult(
                status="blocked",
                plan=plan,
                executed_steps=(),
                message=authorization.message,
            )

            return ExecutionPipelineResult(
                plan=plan,
                orchestration=orchestration,
                dispatch=dispatch,
                authorization=authorization,
                execution=execution,
            )

        execution = self.executor.execute(plan)

        return ExecutionPipelineResult(
            plan=plan,
            orchestration=orchestration,
            dispatch=dispatch,
            authorization=authorization,
            execution=execution,
        )


__all__ = [
    "ExecutionPipeline",
    "ExecutionPipelineResult",
]
