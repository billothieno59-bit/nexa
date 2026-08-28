"""
NEXA Execution Action Handler Tests.
"""

import pytest

from core.execution.executor.handler import ExecutionActionHandler


def test_execution_action_handler_is_abstract():
    """
    The action handler interface must not be directly instantiated.
    """

    with pytest.raises(TypeError):
        ExecutionActionHandler()


def test_execution_action_handler_requires_action_name():
    """
    Concrete handlers must provide an action name.
    """

    class IncompleteHandler(ExecutionActionHandler):
        def handle(self, step):
            pass

    with pytest.raises(TypeError):
        IncompleteHandler()


def test_execution_action_handler_requires_handle():
    """
    Concrete handlers must implement handle().
    """

    class IncompleteHandler(ExecutionActionHandler):
        @property
        def action_name(self):
            return "test"

    with pytest.raises(TypeError):
        IncompleteHandler()


def test_concrete_handler_can_implement_interface():
    """
    A complete handler implementation must be instantiable.
    """

    class TestHandler(ExecutionActionHandler):
        @property
        def action_name(self):
            return "test"

        def handle(self, step):
            return None

    handler = TestHandler()

    assert isinstance(handler, ExecutionActionHandler)
    assert handler.action_name == "test"
