"""
NEXA Africa Operating System
File: core/execution/authorization/policy.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Enforces strict constitutional authorization policies against
             execution plans and granted roles. This module no longer
             imports or calls identity_manager directly — it only
             consumes a caller-supplied set of granted_roles, resolved
             upstream by core/governance/trust/session.py. This keeps
             identity resolution and authorization as separate concerns.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, FrozenSet, Tuple


@dataclass(frozen=True)
class AuthorizationResult:
    """Immutable data container tracking authorization decisions and context mapping status."""

    status: str
    plan: Any
    message: str


class ExecutionAuthorizationPolicy:
    """Evaluates execution plan states and granted roles before clearing operational dispatches."""

    def __init__(self, allowed_actions: Tuple[str, ...]) -> None:
        if not allowed_actions:
            raise ValueError("Allowed actions tuple cannot be empty.")

        seen = set()
        for action in allowed_actions:
            if not isinstance(action, str):
                raise TypeError("All actions inside allowed_actions must be string instances.")
            if not action.strip():
                raise ValueError("Action string elements cannot be blank whitespace.")
            if action in seen:
                raise ValueError(f"Duplicate action detected inside immutable rule ledger: {action}")
            seen.add(action)

        self._allowed_actions: Tuple[str, ...] = allowed_actions

    @property
    def allowed_actions(self) -> Tuple[str, ...]:
        """Exposes the immutable authorized capability sequence mapping list."""
        return self._allowed_actions

    def authorize(self, plan: Any) -> AuthorizationResult:
        """Evaluates incoming plan parameters against the allowed action set."""
        if plan is None:
            raise ValueError("Execution plan context records cannot be null targets.")

        if not hasattr(plan, "status") or not hasattr(plan, "steps"):
            raise TypeError("Provided input target does not conform to a valid ExecutionPlan object standard.")

        if plan.status == "blocked":
            return AuthorizationResult(status="denied", plan=plan, message="Execution plan is blocked.")

        if plan.status == "awaiting_confirmation":
            return AuthorizationResult(status="denied", plan=plan, message="Execution requires confirmation.")

        if plan.status == "ready":
            for step in plan.steps:
                action_name = getattr(step, "action", "")
                if action_name not in self._allowed_actions:
                    return AuthorizationResult(
                        status="denied", plan=plan, message=f"Action is not authorized: {action_name}"
                    )
            return AuthorizationResult(status="authorized", plan=plan, message="Execution plan is authorized.")

        return AuthorizationResult(status="denied", plan=plan, message="Unknown execution state. Failing closed.")

    def authorize_identity_context(
        self,
        requested_intent: str,
        granted_roles: FrozenSet[str],
    ) -> bool:
        """
        Checks whether granted_roles satisfies the role required for
        requested_intent. Does not resolve identity itself — that
        happens upstream in core/governance/trust/session.py. This
        method only checks role membership.
        """
        required_role = "CONSTITUTIONAL_FOUNDER" if "SYSTEM" in requested_intent else "INTERFACE_NODE"
        return required_role in granted_roles


global_policy_engine = ExecutionAuthorizationPolicy(allowed_actions=("respond", "notify"))
