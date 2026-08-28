"""
NEXA Africa Operating System
File: core/cognition/routing/router.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Registers and dispatches named intents to their handlers within cognition.
"""

from __future__ import annotations

from typing import Any, Callable, Dict

from core.services.logging.logger import get_logger

logger = get_logger(__name__)


class RouterHandlerError(Exception):
    """
    Raised when a registered handler itself raises an exception
    during dispatch. Wraps the original exception so the intent
    that failed is always visible in the error.
    """


class SemanticRouter:
    """
    Registers callable handlers against named intents and dispatches
    to them on request.
    """

    def __init__(self) -> None:
        self._handlers: Dict[str, Callable[..., Any]] = {}

    def register(self, intent: str, handler: Callable[..., Any]) -> None:
        """
        Register a handler function for a given intent name.
        """
        self._handlers[intent] = handler

    def dispatch(self, intent: str, **kwargs: Any) -> Any:
        """
        Call the handler registered for the given intent.

        Raises ValueError if no handler is registered.
        Raises RouterHandlerError if the handler itself raises,
        with the original exception logged and chained.
        """
        handler = self._handlers.get(intent)

        if handler is None:
            raise ValueError(f"No handler registered for intent '{intent}'.")

        try:
            return handler(**kwargs)
        except Exception as exc:
            logger.exception(
                "Handler for intent '%s' raised an exception.", intent
            )
            raise RouterHandlerError(
                f"Handler for intent '{intent}' failed: {exc}"
            ) from exc


__all__ = [
    "SemanticRouter",
    "RouterHandlerError",
]
