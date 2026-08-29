from core.applications.api.rate_limiter import TokenBucketRateLimiter
from skills.registry.execution_bridge import invoke_skill


def test_rate_limited_caller_is_denied_before_authorization():
    tight_limiter = TokenBucketRateLimiter(rate=0.0, capacity=1.0)
    tight_limiter.allow_request("attacker")  # consume the only token

    result = invoke_skill(
        caller_id="attacker",
        skill_id="accessibility.simplify_text",
        requested_intent="TEXT.PROCESS",
        rate_limiter=tight_limiter,
    )

    assert result.status == "rate_limited"


def test_caller_within_limit_proceeds_to_authorization():
    generous_limiter = TokenBucketRateLimiter(rate=100.0, capacity=100.0)

    result = invoke_skill(
        caller_id="someone",
        skill_id="nonexistent.skill",
        requested_intent="TEXT.PROCESS",
        rate_limiter=generous_limiter,
    )

    # Not rate-limited — it got far enough to be denied for a different
    # reason (unknown skill), proving the rate limiter let it through.
    assert result.status != "rate_limited"
