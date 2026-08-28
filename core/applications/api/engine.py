"""
NEXA Africa Operating System
File: core/applications/api/engine.py
Constitutional Owner: Bill Odhiambo Othieno
Description: External API entrypoint. Validates and rate-limits requests, then
             delegates resolution to the canonical governed execution gateway.
             This engine never executes handlers directly.
"""

from __future__ import annotations

import hmac
from typing import Any, Dict, Optional

from core.applications.api.rate_limiter import TokenBucketRateLimiter
from core.applications.api.dispatcher import ApiRequestDispatcher


class ApiGatewayEngine:
    """
    Entry point for external requests into NEXA.

    Authenticates and rate-limits incoming requests, then hands
    resolution to the canonical, governed execution gateway via
    ApiRequestDispatcher. Never executes anything directly.
    """

    def __init__(
        self,
        api_key: str,
        rate_limiter: Optional[TokenBucketRateLimiter] = None,
        dispatcher: Optional[ApiRequestDispatcher] = None,
    ) -> None:
        if not api_key or not isinstance(api_key, str):
            raise ValueError(
                "An explicit api_key must be provided. "
                "No default credential is permitted."
            )

        self.api_key = api_key
        self.rate_limiter = rate_limiter or TokenBucketRateLimiter(rate=10.0, capacity=20.0)
        self.dispatcher = dispatcher or ApiRequestDispatcher()

    def authenticate(self, provided_key: str) -> bool:
        """
        Compare the provided key against the configured key using a
        constant-time comparison, so response timing cannot leak
        information about how much of the key matched.
        """
        if not isinstance(provided_key, str):
            return False

        return hmac.compare_digest(provided_key, self.api_key)

    def handle_request(
        self,
        payload: Dict[str, Any],
        auth_key: str,
        client_id: str = "default_client",
    ) -> Dict[str, Any]:
        if not self.authenticate(auth_key):
            return {"status": 401, "error": "Unauthorized: Invalid API key"}

        if not self.rate_limiter.allow_request(client_id):
            return {"status": 429, "error": "Too Many Requests: Rate limit exceeded"}

        return self.dispatcher.dispatch(payload)


__all__ = [
    "ApiGatewayEngine",
]
