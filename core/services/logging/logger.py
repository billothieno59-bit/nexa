"""
NEXA Africa Operating System
File: core/services/logging/logger.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Centralized, structured logging for NEXA. Every subsystem should
             obtain its logger from here instead of configuring logging itself,
             so log format and level stay consistent across the codebase.
"""

from __future__ import annotations

import logging
import os

_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_DEFAULT_LEVEL = "INFO"

_configured_loggers: set[str] = set()


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger for the given module name.

    The log level is controlled by the NEXA_LOG_LEVEL environment
    variable (default INFO). Calling this multiple times for the
    same name never attaches duplicate handlers.
    """

    logger = logging.getLogger(name)

    if name not in _configured_loggers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_LOG_FORMAT))
        logger.addHandler(handler)

        level_name = os.environ.get("NEXA_LOG_LEVEL", _DEFAULT_LEVEL).upper()
        level = getattr(logging, level_name, logging.INFO)
        logger.setLevel(level)

        logger.propagate = False
        _configured_loggers.add(name)

    return logger


__all__ = [
    "get_logger",
]
