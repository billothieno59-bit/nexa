"""
NEXA Africa Operating System
File: core/governance/trust/shutdown/controller.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Authorizes the system.shutdown capability via EmergencyKeyGuard
             and, only when authorized, invokes a supplied callback. Never
             performs the process exit itself, per
             core/contracts/trust/shutdown_contract_v1.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from core.governance.trust.shutdown.key_guard import EmergencyKeyGuard
from core.services.logging.logger import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class ShutdownAuthorization:
    """
    Result of a shutdown authorization attempt. This is the only thing
    the rest of the system should reason about — never the raw key.
    """

    granted: bool
    reason: str


class ShutdownController:
    """
    Gatekeeper for the system.shutdown capability.

    The controller never exits the process itself. A caller supplies a
    shutdown_callback (e.g. a function that calls sys.exit), which is
    only invoked if authorization succeeds. This keeps the controller
    fully testable without ever terminating a real process during tests.
    """

    def __init__(
        self,
        key_guard: Optional[EmergencyKeyGuard] = None,
        shutdown_callback: Optional[Callable[[], None]] = None,
    ) -> None:
        self.key_guard = key_guard or EmergencyKeyGuard()
        self._shutdown_callback = shutdown_callback or (lambda: None)

    def authorize(self, provided_key: str) -> ShutdownAuthorization:
        """
        Check whether the provided key authorizes system.shutdown,
        without performing the shutdown.
        """
        if self.key_guard.verify(provided_key):
            return ShutdownAuthorization(
                granted=True,
                reason="Emergency key verified.",
            )

        return ShutdownAuthorization(
            granted=False,
            reason="Emergency key invalid or not configured.",
        )

    def request_shutdown(self, provided_key: str) -> ShutdownAuthorization:
        """
        Authorize and, if granted, invoke the shutdown callback.
        """
        authorization = self.authorize(provided_key)

        if authorization.granted:
            logger.warning("system.shutdown authorized. Invoking shutdown callback.")
            self._shutdown_callback()
        else:
            logger.warning("system.shutdown denied: %s", authorization.reason)

        return authorization


__all__ = [
    "ShutdownController",
    "ShutdownAuthorization",
]
