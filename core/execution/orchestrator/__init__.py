"""
NEXA Universal Orchestration Layer.

Canonical UOL implementation:

    core.execution.orchestrator
"""

from .orchestrator import ExecutionOrchestrator, OrchestrationResult

__all__ = [
    "ExecutionOrchestrator",
    "OrchestrationResult",
]
