"""
NEXA Africa Operating System
File: core/governance/trust/shutdown/key_guard.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Verifies possession of the emergency shutdown key using a
             constant-time comparison, per
             core/contracts/trust/shutdown_contract_v1.md.

             The expected key is read from the NEXA_EMERGENCY_KEY
             environment variable. It is never hardcoded, and this module
             never logs its value.
"""

from __future__ import annotations

import hmac
import os
import secrets
from typing import Optional

from core.services.logging.logger import get_logger

logger = get_logger(__name__)

EMERGENCY_KEY_ENV_VAR = "NEXA_EMERGENCY_KEY"


class EmergencyKeyGuard:
    """
    Verifies a provided emergency key against the configured secret.

    Fails closed: if no key is configured, verification always denies,
    rather than falling back to any default.
    """

    def __init__(self, expected_key: Optional[str] = None) -> None:
        self.expected_key = expected_key or os.environ.get(EMERGENCY_KEY_ENV_VAR)

    def is_configured(self) -> bool:
        """Whether an expected key is actually set."""
        return bool(self.expected_key)

    def verify(self, provided_key: str) -> bool:
        """
        Constant-time comparison of provided_key against the configured
        key. Never logs either value.
        """
        if not self.is_configured():
            logger.warning(
                "Emergency shutdown key verification attempted but no key is configured."
            )
            return False

        if not isinstance(provided_key, str):
            return False

        result = hmac.compare_digest(provided_key, self.expected_key)

        if result:
            logger.info("Emergency shutdown key verified successfully.")
        else:
            logger.warning("Emergency shutdown key verification failed.")

        return result


def generate_emergency_key() -> str:
    """
    Generate a new cryptographically secure key for use as
    NEXA_EMERGENCY_KEY. This is a convenience for operators — it does not
    store or configure anything itself.
    """
    return secrets.token_urlsafe(32)


__all__ = [
    "EmergencyKeyGuard",
    "generate_emergency_key",
    "EMERGENCY_KEY_ENV_VAR",
]
