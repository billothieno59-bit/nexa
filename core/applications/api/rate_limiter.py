"""
NEXA Africa Operating System
File: core/applications/api/rate_limiter.py
Constitutional Owner: Bill Odhiambo Othieno
Description: In-memory token bucket rate limiter for controlling
             request frequency per client.
"""

from __future__ import annotations

import time
from typing import Dict, Tuple


class TokenBucketRateLimiter:
    """In-memory token bucket algorithm for controlling request frequency per client."""

    def __init__(self, rate: float = 5.0, capacity: float = 10.0):
        self.rate = rate  # Tokens added per second
        self.capacity = capacity  # Maximum bucket capacity
        self._buckets: Dict[str, Tuple[float, float]] = {}  # client_id -> (tokens, last_updated)

    def allow_request(self, client_id: str, tokens_required: float = 1.0) -> bool:
        now = time.time()
        tokens, last_updated = self._buckets.get(client_id, (self.capacity, now))

        elapsed = now - last_updated
        tokens = min(self.capacity, tokens + elapsed * self.rate)

        if tokens >= tokens_required:
            tokens -= tokens_required
            self._buckets[client_id] = (tokens, now)
            return True

        self._buckets[client_id] = (tokens, now)
        return False


__all__ = [
    "TokenBucketRateLimiter",
]
