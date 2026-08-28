"""
NEXA Canonical Registry Skill Integration Tests.
"""

from core.execution.executor.bootstrap import get_handler_registry


def test_canonical_registry_includes_registered_skills():
    registry = get_handler_registry()
    assert registry.get_handler("accessibility.simplify_text") is not None
    assert registry.get_handler("perception.capture_text") is not None
    assert registry.get_handler("system.shutdown_nexa") is not None
