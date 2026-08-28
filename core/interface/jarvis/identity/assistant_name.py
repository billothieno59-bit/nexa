"""
NEXA Canonical Architecture - Interface Layer (JARVIS)
File: core/interface/jarvis/identity/assistant_name.py
Description: Defines the default system-level name and baseline identity configurations.
"""

from typing import Optional


class AssistantIdentity:
    """Manages the fallback identities and core presentation naming properties."""

    DEFAULT_ARCHITECTURAL_NAME: str = "JARVIS"

    def __init__(self, system_name: Optional[str] = None):
        # The underlying system architecture tag is fixed as JARVIS,
        # but the presentation name defaults to it if not customized.
        self._assigned_name: str = system_name or self.DEFAULT_ARCHITECTURAL_NAME

    @property
    def assigned_name(self) -> str:
        """Returns the current user-facing display name for the assistant."""
        return self._assigned_name

    def update_identity_name(self, new_name: str) -> None:
        """Updates the system-level name record when a user renames the assistant."""
        if not new_name.strip():
            raise ValueError("Assistant name cannot be empty or blank whitespace.")
        self._assigned_name = new_name.strip()


# Global baseline identity instance
default_identity = AssistantIdentity()
