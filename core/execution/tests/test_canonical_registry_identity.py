"""
NEXA Canonical Registry Identity Tests.

Proves that ExecutionGateway and ExecutionExecutor both default to the
SAME canonical registry instance from bootstrap.py, rather than each
silently creating their own empty registry.
"""

from core.execution.executor.bootstrap import get_handler_registry
from core.execution.gateway.gateway import ExecutionGateway
from core.execution.executor.executor import ExecutionExecutor


def test_gateway_uses_canonical_registry_by_default():
    canonical = get_handler_registry()
    gateway = ExecutionGateway()
    assert gateway.registry is canonical


def test_executor_uses_canonical_registry_by_default():
    canonical = get_handler_registry()
    executor = ExecutionExecutor()
    assert executor.registry is canonical


def test_gateway_and_executor_share_the_same_registry_instance():
    gateway = ExecutionGateway()
    executor = ExecutionExecutor()
    assert gateway.registry is executor.registry
