from __future__ import annotations

import pytest

from core.execution.authorization.policy import (
    AuthorizationResult,
    ExecutionAuthorizationPolicy,
)
from core.execution.orchestrator.planner.planner import (
    ExecutionPlan,
    PlanStep,
)


def make_plan(
    status: str,
    action: str = "respond",
) -> ExecutionPlan:
    return ExecutionPlan(
        status=status,
        intent="test",
        requires_confirmation=False,
        steps=(
            PlanStep(
                action=action,
            ),
        ),
    )


def test_policy_imports():
    assert ExecutionAuthorizationPolicy is not None
    assert AuthorizationResult is not None


def test_blocked_plan_is_denied():
    policy = ExecutionAuthorizationPolicy(
        allowed_actions=("respond",),
    )

    plan = make_plan("blocked")

    result = policy.authorize(plan)

    assert isinstance(result, AuthorizationResult)
    assert result.status == "denied"
    assert result.plan == plan
    assert result.message == "Execution plan is blocked."


def test_confirmation_plan_is_denied():
    policy = ExecutionAuthorizationPolicy(
        allowed_actions=("respond",),
    )

    plan = make_plan(
        "awaiting_confirmation",
    )

    result = policy.authorize(plan)

    assert isinstance(result, AuthorizationResult)
    assert result.status == "denied"
    assert result.plan == plan
    assert result.message == "Execution requires confirmation."


def test_ready_allowed_action_is_authorized():
    policy = ExecutionAuthorizationPolicy(
        allowed_actions=("respond",),
    )

    plan = make_plan(
        "ready",
        "respond",
    )

    result = policy.authorize(plan)

    assert isinstance(result, AuthorizationResult)
    assert result.status == "authorized"
    assert result.plan == plan
    assert result.message == "Execution plan is authorized."


def test_ready_unknown_action_is_denied():
    policy = ExecutionAuthorizationPolicy(
        allowed_actions=("respond",),
    )

    plan = make_plan(
        "ready",
        "send_email",
    )

    result = policy.authorize(plan)

    assert isinstance(result, AuthorizationResult)
    assert result.status == "denied"
    assert result.plan == plan
    assert result.message == "Action is not authorized: send_email"


def test_unknown_plan_status_fails_closed():
    policy = ExecutionAuthorizationPolicy(
        allowed_actions=("respond",),
    )

    plan = make_plan(
        "something_unknown",
        "respond",
    )

    result = policy.authorize(plan)

    assert isinstance(result, AuthorizationResult)
    assert result.status == "denied"
    assert result.plan == plan
    assert result.message == "Unknown execution state. Failing closed."


def test_invalid_plan_is_rejected():
    policy = ExecutionAuthorizationPolicy(
        allowed_actions=("respond",),
    )

    with pytest.raises((TypeError, ValueError)):
        policy.authorize(None)


def test_allowed_actions_are_immutable():
    policy = ExecutionAuthorizationPolicy(
        allowed_actions=(
            "respond",
            "notify",
        ),
    )

    assert policy.allowed_actions == (
        "respond",
        "notify",
    )


def test_duplicate_allowed_action_is_rejected():
    with pytest.raises(ValueError):
        ExecutionAuthorizationPolicy(
            allowed_actions=(
                "respond",
                "respond",
            ),
        )


def test_invalid_allowed_action_is_rejected():
    with pytest.raises((TypeError, ValueError)):
        ExecutionAuthorizationPolicy(
            allowed_actions=(123,),
        )


def test_empty_allowed_action_is_rejected():
    with pytest.raises(ValueError):
        ExecutionAuthorizationPolicy(
            allowed_actions=("",),
        )
