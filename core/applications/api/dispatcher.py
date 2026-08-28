"""
NEXA Africa Operating System
File: core/applications/api/dispatcher.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Resolve-only request dispatcher for the external API application layer.
             Delegates all action resolution to the canonical ExecutionGateway and
             never invokes handlers directly, per SYSTEM_INSTRUCTION.md's rule that
             the gateway never executes handlers.
"""

from __future__ import annotations

from typing import Any, Dict

from core.execution.gateway.gateway import ExecutionGateway, GatewayRequest


class ApiRequestDispatcher:
    """
    Routes validated external API requests into the canonical,
    governed execution gateway.

    This dispatcher does not execute anything itself. It only
    resolves whether a registered action has a handler, using the
    same ExecutionGateway used by the internal execution pipeline.
    """

    def __init__(self, gateway: ExecutionGateway | None = None) -> None:
        self._gateway = gateway or ExecutionGateway()

    def dispatch(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve an external request against the canonical registry.

        Never invokes a handler. Only reports whether one is
        registered and ready for a future, separately-governed
        execution step.
        """

        action = payload.get("action")

        if not isinstance(action, str) or not action.strip():
            return {
                "status": 400,
                "error": "Bad Request: Missing or invalid action.",
            }

        parameters = payload.get("params", {})

        request = GatewayRequest(action=action, parameters=parameters)
        result = self._gateway.resolve(request)

        if result.status == "resolved":
            return {
                "status": 200,
                "message": f"Action '{action}' resolved and pending governed execution.",
                "action": action,
            }

        if result.status == "blocked":
            return {
                "status": 404,
                "error": f"Handler not found for action '{action}'.",
            }

        return {
            "status": 400,
            "error": result.message,
        }


__all__ = [
    "ApiRequestDispatcher",
]
