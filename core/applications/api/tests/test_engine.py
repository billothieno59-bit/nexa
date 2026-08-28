"""
NEXA Application API Engine Tests.
"""

import pytest

from core.applications.api.engine import ApiGatewayEngine
from core.applications.api.rate_limiter import TokenBucketRateLimiter
from core.applications.api.dispatcher import ApiRequestDispatcher
from core.execution.gateway.gateway import ExecutionGateway
from core.execution.executor.bootstrap import get_handler_registry


@pytest.fixture
def engine():
    limiter = TokenBucketRateLimiter(rate=10.0, capacity=10.0)
    gateway = ExecutionGateway(registry=get_handler_registry())
    dispatcher = ApiRequestDispatcher(gateway=gateway)
    return ApiGatewayEngine(api_key="nexa_test_key", rate_limiter=limiter, dispatcher=dispatcher)


def test_engine_requires_explicit_api_key():
    with pytest.raises(ValueError):
        ApiGatewayEngine(api_key="")


def test_engine_resolves_registered_action(engine):
    payload = {"action": "INTENT_SYSTEM_DIAGNOSTIC_CHECK"}
    response = engine.handle_request(payload, auth_key="nexa_test_key")
    assert response["status"] == 200


def test_engine_unregistered_action_not_found(engine):
    payload = {"action": "custom_event"}
    response = engine.handle_request(payload, auth_key="nexa_test_key")
    assert response["status"] == 404


def test_engine_auth_failure(engine):
    payload = {"action": "INTENT_SYSTEM_DIAGNOSTIC_CHECK"}
    response = engine.handle_request(payload, auth_key="bad_key")
    assert response["status"] == 401


def test_engine_missing_action(engine):
    response = engine.handle_request({}, auth_key="nexa_test_key")
    assert response["status"] == 400
