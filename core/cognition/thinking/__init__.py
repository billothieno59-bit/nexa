"""
NEXA Cognition Thinking subsystem.

This package contains reasoning and decision-processing
components belonging to the canonical cognition layer.

Canonical path:

    core.cognition.thinking
"""

from .decision_engine import Decision

__all__ = [
    "Decision",
]
