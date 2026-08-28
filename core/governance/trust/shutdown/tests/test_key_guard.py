"""
NEXA EmergencyKeyGuard Tests.
"""

from core.governance.trust.shutdown.key_guard import (
    EmergencyKeyGuard,
    generate_emergency_key,
)


def test_verify_succeeds_with_correct_key():
    guard = EmergencyKeyGuard(expected_key="correct-key-123")
    assert guard.verify("correct-key-123") is True


def test_verify_fails_with_incorrect_key():
    guard = EmergencyKeyGuard(expected_key="correct-key-123")
    assert guard.verify("wrong-key") is False


def test_verify_fails_closed_when_unconfigured():
    guard = EmergencyKeyGuard(expected_key=None)
    assert guard.is_configured() is False
    assert guard.verify("anything") is False


def test_verify_rejects_non_string_input():
    guard = EmergencyKeyGuard(expected_key="correct-key-123")
    assert guard.verify(12345) is False


def test_generate_emergency_key_produces_distinct_keys():
    key_a = generate_emergency_key()
    key_b = generate_emergency_key()
    assert key_a != key_b
    assert len(key_a) > 20
