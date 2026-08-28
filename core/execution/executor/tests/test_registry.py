"""
NEXA Execution Handler Registry Tests.
"""

import pytest

from core.execution.executor.handler import ExecutionActionHandler
from core.execution.executor.registry import HandlerRegistry


class RegistryTestHandler(ExecutionActionHandler):
    """
    Simple test handler used to verify registry behavior.
    """

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def action_name(self) -> str:
        return self._name

    def handle(self, step) -> None:
        return None


def test_registry_imports_and_instantiates():
    """
    HandlerRegistry must import and instantiate correctly.
    """

    registry = HandlerRegistry()

    assert isinstance(registry, HandlerRegistry)
    assert len(registry) == 0


def test_registry_accepts_valid_handler():
    """
    A valid ExecutionActionHandler can be registered.
    """

    handler = RegistryTestHandler("respond")

    registry = HandlerRegistry(
        handlers=(handler,),
    )

    assert len(registry) == 1
    assert registry.has_handler("respond") is True
    assert registry.get_handler("respond") is handler


def test_registry_returns_none_for_unknown_handler():
    """
    Unknown actions must not resolve to a handler.
    """

    registry = HandlerRegistry()

    assert registry.has_handler("unknown") is False
    assert registry.get_handler("unknown") is None


def test_registry_rejects_invalid_handler():
    """
    Registry must reject objects that do not implement
    ExecutionActionHandler.
    """

    with pytest.raises(TypeError):
        HandlerRegistry(
            handlers=("not a handler",),
        )


def test_registry_rejects_duplicate_action_names():
    """
    Two handlers cannot claim the same canonical action name.
    """

    first = RegistryTestHandler("respond")
    second = RegistryTestHandler("respond")

    with pytest.raises(ValueError):
        HandlerRegistry(
            handlers=(first, second),
        )


def test_registry_rejects_empty_action_name():
    """
    Handler action names cannot be empty.
    """

    handler = RegistryTestHandler("")

    with pytest.raises(ValueError):
        HandlerRegistry(
            handlers=(handler,),
        )


def test_registry_rejects_non_string_action_name():
    """
    Handler action names must be strings.
    """

    class InvalidHandler(ExecutionActionHandler):
        @property
        def action_name(self):
            return 123

        def handle(self, step) -> None:
            return None

    with pytest.raises(TypeError):
        HandlerRegistry(
            handlers=(InvalidHandler(),),
        )


def test_registered_actions_are_immutable():
    """
    registered_actions() must return an immutable tuple.
    """

    handler = RegistryTestHandler("respond")

    registry = HandlerRegistry(
        handlers=(handler,),
    )

    actions = registry.registered_actions()

    assert isinstance(actions, tuple)
    assert actions == ("respond",)


def test_registry_is_immutable():
    """
    HandlerRegistry itself must be immutable.
    """

    handler = RegistryTestHandler("respond")

    registry = HandlerRegistry(
        handlers=(handler,),
    )

    with pytest.raises(Exception):
        registry._handlers = {}


def test_registry_does_not_execute_handlers():
    """
    Looking up a handler must never execute it.
    """

    class TrackingHandler(ExecutionActionHandler):
        def __init__(self) -> None:
            self.called = False

        @property
        def action_name(self) -> str:
            return "test"

        def handle(self, step) -> None:
            self.called = True

    handler = TrackingHandler()

    registry = HandlerRegistry(
        handlers=(handler,),
    )

    resolved = registry.get_handler("test")

    assert resolved is handler
    assert handler.called is False
