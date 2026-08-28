"""
NEXA Cognition subsystem.

Canonical cognition root:

    core.cognition

Cognition is responsible for reasoning, planning, memory,
learning, and decision processes.

Architectural boundary:

    Semantic Meaning
           |
           v
       Cognition
           |
           v
    Decision / Reasoning
           |
           v
       Execution

Cognition must remain independent of human-language
presentation and must not absorb responsibilities owned
by communication, semantics, governance, or execution.
"""

from . import thinking

__all__ = [
    "thinking",
]
