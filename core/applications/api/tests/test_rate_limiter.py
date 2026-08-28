"""
NEXA Application API Rate Limiter Tests.
"""

import time
import pytest
from core.applications.api.rate_limiter import TokenBucketRateLimiter


@pytest.fixture
def limiter():
    return TokenBucketRateLimiter(rate=2.0, capacity=2.0)


def test_rate_limiter_allows_initial_burst(limiter):
    client = "client_alpha"
    assert limiter.allow_request(client) is True
    assert limiter.allow_request(client) is True
    # Bucket depleted
    assert limiter.allow_request(client) is False


def test_rate_limiter_refills_over_time(limiter):
    client = "client_beta"
    limiter.allow_request(client)
    limiter.allow_request(client)
    assert limiter.allow_request(client) is False

    # Wait for refill
    time.sleep(0.6)
    assert limiter.allow_request(client) is True
