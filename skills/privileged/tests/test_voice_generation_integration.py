"""
NEXA Voice Generation — End-to-End Integration Test.

Proves generation.voice works through the FULL real governed pipeline
(invoke_skill -> rate limit -> trust session -> authorization) rather
than only through SkillAuthorizationGate in isolation. Only the actual
network-calling ElevenLabs client is faked (network calls are not made
in tests) — every layer of NEXA's own logic runs for real.
"""

from core.applications.api.rate_limiter import TokenBucketRateLimiter
from skills.registry.execution_bridge import invoke_skill
from skills.registry.registry import SkillRegistry
from skills.privileged.voice_generation import register_privileged_skills
from core.generation.providers.voice_router import get_voice_provider


FOUNDER_ID = "founder_root_001"  # bootstrapped CONSTITUTIONAL_FOUNDER identity


def _registry_with_voice_skill():
    registry = SkillRegistry()
    register_privileged_skills(registry)
    return registry


def test_founder_can_generate_voice_through_full_pipeline(monkeypatch):
    """
    'Welcome back, Bill.' flowing through: rate limit -> trust session
    resolution -> CONSTITUTIONAL_FOUNDER role match -> VOICE.GENERATE
    permission -> generation.voice skill -> ElevenLabsVoiceProvider.
    Only the actual outbound network call is faked.
    """
    registry = _registry_with_voice_skill()
    generous_limiter = TokenBucketRateLimiter(rate=100.0, capacity=100.0)

    provider = get_voice_provider("elevenlabs")
    monkeypatch.setattr(
        provider,
        "generate",
        lambda text: {"status": "ok", "audio_bytes_length": 1234, "provider": "elevenlabs"},
    )
    monkeypatch.setattr(
        "skills.privileged.voice_generation.get_voice_provider",
        lambda name=None: provider,
    )

    result = invoke_skill(
        caller_id=FOUNDER_ID,
        skill_id="generation.voice",
        requested_intent="SYSTEM.WELCOME_GREETING",
        registry=registry,
        rate_limiter=generous_limiter,
        text="Welcome back, Bill.",
    )

    assert result.status == "executed"
    assert result.result["status"] == "ok"


def test_non_founder_identity_is_denied_through_full_pipeline():
    """
    An identity with no registered profile (or a non-founder role) must
    be denied by real trust/authorization resolution — not by a test
    fake — proving VOICE.GENERATE is genuinely founder-only end to end.
    """
    registry = _registry_with_voice_skill()
    generous_limiter = TokenBucketRateLimiter(rate=100.0, capacity=100.0)

    result = invoke_skill(
        caller_id="unknown_visitor_id",
        skill_id="generation.voice",
        requested_intent="SYSTEM.WELCOME_GREETING",
        registry=registry,
        rate_limiter=generous_limiter,
        text="Welcome back, Bill.",
    )

    assert result.status == "denied"


def test_founder_is_rate_limited_before_reaching_voice_generation():
    """
    Proves rate limiting is enforced ahead of authorization for this
    specific skill too, not just in the generic tests added earlier.
    """
    registry = _registry_with_voice_skill()
    exhausted_limiter = TokenBucketRateLimiter(rate=0.0, capacity=1.0)
    exhausted_limiter.allow_request(FOUNDER_ID)  # consume the only token

    result = invoke_skill(
        caller_id=FOUNDER_ID,
        skill_id="generation.voice",
        requested_intent="SYSTEM.WELCOME_GREETING",
        registry=registry,
        rate_limiter=exhausted_limiter,
        text="Welcome back, Bill.",
    )

    assert result.status == "rate_limited"


def test_founder_without_intent_containing_system_is_denied():
    """
    Documents existing (not new) behavior: resolve_trust_session() only
    grants CONSTITUTIONAL_FOUNDER when 'SYSTEM' appears in the requested
    intent string. A founder calling with an unrelated intent string is
    still denied — this is pre-existing coupling, not something this
    test introduces.
    """
    registry = _registry_with_voice_skill()
    generous_limiter = TokenBucketRateLimiter(rate=100.0, capacity=100.0)

    result = invoke_skill(
        caller_id=FOUNDER_ID,
        skill_id="generation.voice",
        requested_intent="GREETING.PLAY",
        registry=registry,
        rate_limiter=generous_limiter,
        text="Welcome back, Bill.",
    )

    assert result.status == "denied"
