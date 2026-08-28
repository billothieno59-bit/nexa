"""
NEXA ShutdownController Tests.
"""

from core.governance.trust.shutdown.controller import (
    ShutdownController,
    ShutdownAuthorization,
)
from core.governance.trust.shutdown.key_guard import EmergencyKeyGuard


def test_authorize_grants_with_correct_key():
    guard = EmergencyKeyGuard(expected_key="secret")
    controller = ShutdownController(key_guard=guard)

    result = controller.authorize("secret")
    assert isinstance(result, ShutdownAuthorization)
    assert result.granted is True


def test_authorize_denies_with_incorrect_key():
    guard = EmergencyKeyGuard(expected_key="secret")
    controller = ShutdownController(key_guard=guard)

    result = controller.authorize("wrong")
    assert result.granted is False


def test_request_shutdown_invokes_callback_only_when_authorized():
    guard = EmergencyKeyGuard(expected_key="secret")
    calls = []
    controller = ShutdownController(
        key_guard=guard,
        shutdown_callback=lambda: calls.append("shutdown_invoked"),
    )

    controller.request_shutdown("wrong")
    assert calls == []

    controller.request_shutdown("secret")
    assert calls == ["shutdown_invoked"]


def test_request_shutdown_never_invokes_callback_when_unconfigured():
    guard = EmergencyKeyGuard(expected_key=None)
    calls = []
    controller = ShutdownController(
        key_guard=guard,
        shutdown_callback=lambda: calls.append("shutdown_invoked"),
    )

    controller.request_shutdown("anything")
    assert calls == []
