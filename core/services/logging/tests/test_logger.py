"""
NEXA Logging Utility Tests.
"""

import logging

from core.services.logging.logger import get_logger


def test_get_logger_returns_logger_instance():
    logger = get_logger("test.module.one")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test.module.one"


def test_get_logger_does_not_duplicate_handlers():
    logger_a = get_logger("test.module.two")
    logger_b = get_logger("test.module.two")

    assert logger_a is logger_b
    assert len(logger_a.handlers) == 1


def test_get_logger_does_not_propagate_to_root():
    logger = get_logger("test.module.three")
    assert logger.propagate is False
