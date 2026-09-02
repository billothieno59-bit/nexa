from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseMemoryAdapter(ABC):
    """Abstract interface for Nexa OS persistent memory storage."""

    @abstractmethod
    def save(self, key: str, value: Dict[str, Any]) -> bool:
        """Persist a memory entry by unique key."""
        pass

    @abstractmethod
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve a memory entry by key."""
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete a memory entry by key."""
        pass

    @abstractmethod
    def list_all(self) -> List[Dict[str, Any]]:
        """List all stored memory records."""
        pass
