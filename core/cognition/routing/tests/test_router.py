import pytest
from core.cognition.routing.router import SemanticRouter, RouterHandlerError


@pytest.fixture
def router():
    return SemanticRouter()


def test_register_and_dispatch(router):
    def echo_handler(message: str):
        return f"Processed: {message}"

    router.register("echo", echo_handler)
    result = router.dispatch("echo", message="hello world")
    assert result == "Processed: hello world"


def test_unregistered_intent_raises(router):
    with pytest.raises(ValueError, match="No handler registered"):
        router.dispatch("unknown_action")


def test_handler_exception_is_wrapped_and_logged(router):
    def broken_handler():
        raise RuntimeError("boom")

    router.register("broken", broken_handler)

    with pytest.raises(RouterHandlerError, match="boom"):
        router.dispatch("broken")
