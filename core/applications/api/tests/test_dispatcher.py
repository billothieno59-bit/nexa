"""
NEXA Application API Dispatcher Tests.
"""

from core.applications.api.dispatcher import ApiRequestDispatcher
from core.execution.gateway.gateway import ExecutionGateway
from core.execution.executor.bootstrap import get_handler_registry


def make_dispatcher():
    gateway = ExecutionGateway(registry=get_handler_registry())
    return ApiRequestDispatcher(gateway=gateway)


def test_dispatcher_resolves_registered_action():
    dispatcher = make_dispatcher()
    res = dispatcher.dispatch({"action": "INTENT_SYSTEM_DIAGNOSTIC_CHECK"})
    assert res["status"] == 200
    assert "resolved" in res["message"]


def test_dispatcher_unregistered_action_is_not_found():
    dispatcher = make_dispatcher()
    res = dispatcher.dispatch({"action": "INTENT_UNKNOWN_ACTION"})
    assert res["status"] == 404


def test_dispatcher_missing_action_is_rejected():
    dispatcher = make_dispatcher()
    res = dispatcher.dispatch({})
    assert res["status"] == 400


def test_dispatcher_never_executes_a_handler():
    """
    The dispatcher must never invoke a Python callable directly.
    It only reports whether a handler is registered.
    """
    dispatcher = make_dispatcher()
    res = dispatcher.dispatch({"action": "INTENT_SYSTEM_DIAGNOSTIC_CHECK"})
    assert "result" not in res
