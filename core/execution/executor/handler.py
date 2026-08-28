"""
NEXA Execution Action Handler Interface.

This module defines the controlled boundary between the
NEXA Execution Executor and future action implementations.

IMPORTANT
---------
Handlers are intentionally abstract at this stage.

This interface does NOT:

- execute operating-system commands
- access the network
- modify files
- control devices
- launch applications
- perform external side effects

Future handlers must be explicitly registered and invoked
through the controlled execution architecture.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from core.execution.orchestrator.planner.planner import PlanStep


class ExecutionActionHandler(ABC):
    """
    Abstract interface for a controlled NEXA action handler.

    Every future executable action must implement this
    interface before it can be considered by the executor.
    """

    @property
    @abstractmethod
    def action_name(self) -> str:
        """
        Return the canonical action name handled by this handler.
        """
        raise NotImplementedError

    @abstractmethod
    def handle(self, step: PlanStep) -> None:
        """
        Handle one execution step.

        The initial architecture intentionally provides no
        concrete side-effect implementation.
        """
        raise NotImplementedError
