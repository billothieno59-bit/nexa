"""
NEXA Africa Operating System
File: core/cognition/memory/manager.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Session-memory manager that delegates persistence to a pluggable
             memory adapter (e.g. SQLiteMemoryAdapter).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.cognition.memory.adapters.sqlite_adapter import SQLiteMemoryAdapter


class MemoryManager:
    """
    Manages agent session memory by delegating storage to an adapter.

    The manager itself holds no storage logic. It only defines the
    session-memory vocabulary (store/retrieve/list/forget) and forwards
    calls to whatever adapter is supplied.
    """

    def __init__(self, adapter: Optional[Any] = None) -> None:
        self.adapter = adapter or SQLiteMemoryAdapter()

    def store_memory(self, session_id: str, payload: Dict[str, Any]) -> bool:
        """
        Store a session's memory payload.
        """
        return self.adapter.save(session_id, payload)

    def retrieve_memory(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a session's memory payload, or None if not found.
        """
        return self.adapter.get(session_id)

    def list_memories(self) -> List[Dict[str, Any]]:
        """
        List all stored memory payloads.
        """
        return self.adapter.list_all()

    def forget_memory(self, session_id: str) -> bool:
        """
        Remove a session's memory payload.
        """
        return self.adapter.delete(session_id)


__all__ = [
    "MemoryManager",
]
