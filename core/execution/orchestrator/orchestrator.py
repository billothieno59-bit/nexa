
"""
NEXA Africa Operating System
File: core/execution/orchestrator/orchestrator.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Orchestrates multi-layered planning matrices. Resolves an
             identity's TrustSession first (via core/governance/trust/session.py),
             then passes only the granted roles into authorization policy
             — never the raw identity — keeping identity resolution and
             authorization as separate concerns.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Tuple

from core.execution.orchestrator.planner.planner import (
    ExecutionPlanner,
    ExecutionPlan,
)

from core.execution.authorization.policy import global_policy_engine
from core.governance.trust.signature.guard_engine import global_trust_guard
from core.governance.trust.session import resolve_trust_session


@dataclass(frozen=True)
class OrchestrationResult:
    """
    Structured result produced by the execution orchestrator.
    """

    status: str
    intent: str = "unknown"
    steps: Tuple[Any, ...] = field(default_factory=tuple)
    reason: str = ""
    plan: Optional[ExecutionPlan] = None
    message: str = ""

    def __post_init__(self) -> None:
        """
        Keep the flat and structured representations synchronized.
        """

        if self.plan is None:
            object.__setattr__(
                self,
                "plan",
                ExecutionPlan(
                    status=self.status,
                    intent=self.intent,
                    requires_confirmation=(
                        "confirmation" in self.status
                    ),
                    steps=tuple(self.steps),
                    reason=self.reason,
                ),
            )
        else:
            object.__setattr__(
                self,
                "intent",
                self.plan.intent,
            )

            object.__setattr__(
                self,
                "steps",
                tuple(self.plan.steps),
            )

            object.__setattr__(
                self,
                "reason",
                self.plan.reason,
            )

        if not self.message:
            if self.status == "blocked":
                message = "Execution plan is blocked."
            elif self.status == "awaiting_confirmation":
                message = "Confirmation is required before execution."
            elif self.status == "ready":
                message = "Execution plan is ready."
            else:
                message = "Execution plan is blocked."

            object.__setattr__(
                self,
                "message",
                message,
            )


class ExecutionOrchestrator:
    """
    Coordinates incoming operational requests.

    The orchestrator accepts either:

    - a canonical Decision, or
    - an already-created ExecutionPlan.

    This allows the pipeline to preserve the correct architectural
    order without creating the same plan twice.
    """

    def __init__(
        self,
        policy_engine: Optional[Any] = None,
    ) -> None:
        self.policy = (
            policy_engine
            or global_policy_engine
        )

        self.trust_guard = global_trust_guard

        self.planner = ExecutionPlanner()

    def orchestrate(
        self,
        decision: Any,
    ) -> OrchestrationResult:
        """
        Convert a Decision or ExecutionPlan into an orchestration result.

        A pre-built ExecutionPlan is preserved exactly.

        A Decision is converted through the canonical planner.
        """

        if decision is None:
            raise ValueError(
                "Cognition decision context cannot be null."
            )

        if isinstance(decision, ExecutionPlan):
            plan = decision
        else:
            plan = self.planner.create_plan(decision)

        reason = (
            getattr(decision, "reason", "")
            or plan.reason
        )

        if plan.status == "blocked":
            return OrchestrationResult(
                status="blocked",
                plan=plan,
                reason=(
                    reason
                    or "Blocked by governance."
                ),
            )

        if plan.status == "awaiting_confirmation":
            return OrchestrationResult(
                status="awaiting_confirmation",
                plan=plan,
                reason=(
                    reason
                    or "Confirmation required."
                ),
            )

        if plan.status == "ready":
            return OrchestrationResult(
                status="ready",
                plan=plan,
                reason=(
                    reason
                    or "No external side effect."
                ),
            )

        return OrchestrationResult(
            status="blocked",
            plan=plan,
            reason="Unknown execution state.",
        )

    def process_governed_request(
        self,
        caller_id: str,
        intent_token: str,
        plan_context: Any,
    ) -> Dict[str, Any]:
        """
        Validate identity, trust, and execution authorization
        before allowing governed dry-run processing.

        Identity is resolved into a TrustSession first (trust layer),
        then only the resulting granted roles are passed into
        authorization policy — never the raw identity.
        """

        trust_session = resolve_trust_session(caller_id, intent_token)

        identity_cleared = self.policy.authorize_identity_context(
            intent_token,
            trust_session.granted_roles,
        )

        if not identity_cleared:
            return {
                "success": False,
                "status": "DENIED_IDENTITY_INVALID",
                "error": (
                    f"Caller identity {caller_id} "
                    "failed authorization constraints."
                ),
                "execution_boundary": "CLOSED",
            }

        signature = (
            self.trust_guard.generate_payload_signature(
                intent_token
            )
        )

        trust_report = (
            self.trust_guard.verify_contract_integrity(
                intent_token,
                signature,
            )
        )

        if not trust_report["verified"]:
            return {
                "success": False,
                "status": "DENIED_TRUST_CORRUPTED",
                "error": (
                    "Contract hash signature "
                    "verification failure."
                ),
                "execution_boundary": "CLOSED",
            }

        plan_report = self.policy.authorize(
            plan_context
        )

        if plan_report.status != "authorized":
            return {
                "success": False,
                "status": (
                    "DENIED_PLAN_"
                    f"{plan_report.status.upper()}"
                ),
                "error": plan_report.message,
                "execution_boundary": "CLOSED",
            }

        return {
            "success": True,
            "status": "PLAN_ORCHESTRATION_AUTHORIZED",
            "message": (
                "Execution pipeline authorized "
                "for dry-run processing."
            ),
            "execution_boundary": "VERIFIED",
        }


__all__ = [
    "ExecutionOrchestrator",
    "OrchestrationResult",
]
