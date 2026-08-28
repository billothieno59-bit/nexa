"""
NEXA Execution Gateway.

The gateway is the final controlled resolution boundary before
future concrete execution handlers.

Architectural boundary:

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
    Executor
        |
        v
    Execution Gateway
        |
        v
    Handler Registry
        |
        v
    Future Action Handlers

The gateway does NOT execute handlers.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from core.execution.executor.handler import ExecutionActionHandler
from core.execution.executor.registry import HandlerRegistry
from core.execution.executor.bootstrap import get_handler_registry


@dataclass(frozen=True)
class GatewayRequest:
    """
    Represents a request entering the execution gateway.
    """

    action: str
    parameters: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class GatewayResult:
    """
    Result produced by the execution gateway.
    """

    status: str
    action: str
    message: str
    handler: ExecutionActionHandler | None = None


class ExecutionGateway:
    """
    Controlled resolution boundary.

    The gateway resolves handlers from the canonical registry
    but never executes them.
    """

    def __init__(
        self,
        registry: HandlerRegistry | None = None,
    ) -> None:
        """
        Initialize the gateway.

        If no registry is supplied, use the canonical registry from
        bootstrap.py, so every component sees the same registered
        handlers by default. If a registry is supplied explicitly
        (e.g. in tests), preserve that exact instance instead.
        """

        self._registry = registry if registry is not None else get_handler_registry()

    @property
    def registry(self) -> HandlerRegistry:
        """
        Return the canonical registry instance.
        """

        return self._registry

    def resolve(
        self,
        request: GatewayRequest,
    ) -> GatewayResult:
        """
        Resolve a request without executing anything.
        """

        if not isinstance(request, GatewayRequest):
            raise TypeError("request must be a GatewayRequest.")

        action = request.action

        if not isinstance(action, str) or not action.strip():
            return GatewayResult(
                status="rejected",
                action=str(action),
                message="Invalid action.",
            )

        handler = self._registry.get_handler(action)

        if handler is None:
            return GatewayResult(
                status="blocked",
                action=action,
                message="Action is not registered.",
            )

        return GatewayResult(
            status="resolved",
            action=action,
            message="Action handler resolved.",
            handler=handler,
        )

    def execute(
        self,
        request: GatewayRequest,
    ) -> GatewayResult:
        """
        Direct execution is intentionally forbidden.
        """

        if not isinstance(request, GatewayRequest):
            raise TypeError("request must be a GatewayRequest.")

        return GatewayResult(
            status="blocked",
            action=request.action,
            message="Direct gateway execution is not permitted.",
        )


__all__ = [
    "ExecutionGateway",
    "GatewayRequest",
    "GatewayResult",
]
