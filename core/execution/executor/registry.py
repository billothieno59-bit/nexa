"""
NEXA Execution Handler Registry.

The handler registry provides a controlled allow-list for
execution action handlers.

IMPORTANT
---------
The registry does not execute handlers.

It only:

- registers approved handler instances
- prevents duplicate action names
- resolves handlers by canonical action name
- reports whether an action is registered
- keeps the handler collection controlled

Actual execution remains the responsibility of the
ExecutionExecutor and its future authorization boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from core.execution.executor.handler import ExecutionActionHandler


@dataclass(frozen=True)
class HandlerRegistry:
    """
    Immutable registry of approved execution handlers.

    The registry stores handlers by their canonical action name.
    """

    _handlers: Mapping[str, ExecutionActionHandler]

    def __init__(
        self,
        handlers: tuple[ExecutionActionHandler, ...] = (),
    ) -> None:
        registry: dict[str, ExecutionActionHandler] = {}

        for handler in handlers:
            self._validate_handler(handler)

            action_name = handler.action_name

            if action_name in registry:
                raise ValueError(f"Handler already registered for action: {action_name}")

            registry[action_name] = handler

        object.__setattr__(self, "_handlers", registry)

    @staticmethod
    def _validate_handler(
        handler: ExecutionActionHandler,
    ) -> None:
        """
        Validate that a registry entry implements the
        controlled action-handler interface.
        """

        if not isinstance(handler, ExecutionActionHandler):
            raise TypeError("HandlerRegistry requires ExecutionActionHandler instances.")

        action_name = handler.action_name

        if not isinstance(action_name, str):
            raise TypeError("Execution handler action_name must be a string.")

        if not action_name.strip():
            raise ValueError("Execution handler action_name cannot be empty.")

    def has_handler(self, action_name: str) -> bool:
        """
        Return True when a handler is registered for action_name.
        """

        if not isinstance(action_name, str):
            raise TypeError("action_name must be a string.")

        return action_name in self._handlers

    def get_handler(
        self,
        action_name: str,
    ) -> ExecutionActionHandler | None:
        """
        Resolve a registered handler by action name.

        Returns None when no handler is registered.
        """

        if not isinstance(action_name, str):
            raise TypeError("action_name must be a string.")

        return self._handlers.get(action_name)

    def registered_actions(self) -> tuple[str, ...]:
        """
        Return all registered action names.

        The returned collection is immutable.
        """

        return tuple(self._handlers.keys())

    def __len__(self) -> int:
        """
        Return the number of registered handlers.
        """

        return len(self._handlers)


__all__ = [
    "HandlerRegistry",
]
