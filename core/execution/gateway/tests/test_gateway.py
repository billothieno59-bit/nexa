from __future__ import annotations

from core.execution.executor.handler import ExecutionActionHandler
from core.execution.executor.registry import HandlerRegistry
from core.execution.gateway.gateway import (
    ExecutionGateway,
    GatewayRequest,
)


class GatewayTestHandler(ExecutionActionHandler):
    """
    Test helper.

    Pytest will NOT collect this class because its
    name no longer starts with 'Test'.
    """

    def __init__(self, action_name: str):
        self._action_name = action_name
        self.executed = False

    @property
    def action_name(self) -> str:
        return self._action_name

    def handle(self, parameters: dict[str, object]) -> object:
        self.executed = True
        return parameters


def test_gateway_imports():
    gateway = ExecutionGateway()

    assert isinstance(gateway, ExecutionGateway)


def test_gateway_uses_canonical_registry():
    registry = HandlerRegistry()

    gateway = ExecutionGateway(registry)

    assert gateway.registry is registry


def test_valid_request_is_resolved():
    handler = GatewayTestHandler("respond")

    registry = HandlerRegistry(
        handlers=(handler,),
    )

    gateway = ExecutionGateway(registry)

    result = gateway.resolve(GatewayRequest(action="respond"))

    assert result.status == "resolved"
    assert result.handler is handler
    assert handler.executed is False


def test_unknown_action_is_blocked():
    gateway = ExecutionGateway()

    result = gateway.resolve(GatewayRequest(action="missing_action"))

    assert result.status == "blocked"
    assert result.handler is None


def test_invalid_request_is_rejected():
    gateway = ExecutionGateway()

    try:
        gateway.resolve("not a request")
        assert False
    except TypeError:
        assert True


def test_invalid_action_is_rejected():
    gateway = ExecutionGateway()

    result = gateway.resolve(GatewayRequest(action=""))

    assert result.status == "rejected"


def test_gateway_resolves_handler_from_registry():
    handler = GatewayTestHandler("respond")

    registry = HandlerRegistry(
        handlers=(handler,),
    )

    gateway = ExecutionGateway(registry)

    result = gateway.resolve(GatewayRequest(action="respond"))

    assert result.handler is handler


def test_gateway_never_executes_handlers():
    handler = GatewayTestHandler("respond")

    registry = HandlerRegistry(
        handlers=(handler,),
    )

    gateway = ExecutionGateway(registry)

    gateway.resolve(GatewayRequest(action="respond"))

    assert handler.executed is False


def test_direct_gateway_execution_is_blocked():
    handler = GatewayTestHandler("respond")

    registry = HandlerRegistry(
        handlers=(handler,),
    )

    gateway = ExecutionGateway(registry)

    result = gateway.execute(GatewayRequest(action="respond"))

    assert result.status == "blocked"
    assert handler.executed is False


def test_gateway_result_is_immutable():
    from dataclasses import FrozenInstanceError

    handler = GatewayTestHandler("respond")

    registry = HandlerRegistry(
        handlers=(handler,),
    )

    gateway = ExecutionGateway(registry)

    result = gateway.resolve(GatewayRequest(action="respond"))

    try:
        result.status = "changed"
        assert False
    except FrozenInstanceError:
        assert True
