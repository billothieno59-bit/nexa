"""
NEXA Africa Operating System
File: core/interface/jarvis/identity/name_selection.py
Description: Controls the public-facing presentation name of the Jarvis interface.
"""

from __future__ import annotations

from typing import Any

from core.interface.jarvis.identity.assistant_name import default_identity


class NameSelectionManager:
    """
    Manages the user-visible assistant name.

    This affects presentation only and never changes the
    constitutional architecture of NEXA.
    """

    MIN_NAME_LENGTH = 2
    MAX_NAME_LENGTH = 40

    def __init__(self) -> None:
        self.selection_history: list[str] = []

    def set_custom_name(self, custom_name: str) -> dict[str, Any]:
        """
        Assign a custom presentation name.
        """

        if not isinstance(custom_name, str):
            return {
                "success": False,
                "name": default_identity.assigned_name,
                "error": "Assistant name must be a string.",
            }

        cleaned_name = custom_name.strip()

        if not self.MIN_NAME_LENGTH <= len(cleaned_name) <= self.MAX_NAME_LENGTH:
            return {
                "success": False,
                "name": default_identity.assigned_name,
                "error": (
                    f"Assistant name must be between {self.MIN_NAME_LENGTH} and {self.MAX_NAME_LENGTH} characters."
                ),
            }

        default_identity.update_identity_name(cleaned_name)

        self.selection_history.append(cleaned_name)

        return {
            "success": True,
            "name": default_identity.assigned_name,
            "error": None,
        }

    def reset_to_default(self) -> str:
        """
        Restore the default architectural presentation name.
        """

        default_identity.update_identity_name(default_identity.DEFAULT_ARCHITECTURAL_NAME)

        self.selection_history.append(default_identity.DEFAULT_ARCHITECTURAL_NAME)

        return default_identity.assigned_name

    def current_name(self) -> str:
        """
        Return the active presentation name.
        """

        return default_identity.assigned_name

    def history(self) -> tuple[str, ...]:
        """
        Return an immutable history of chosen names.
        """

        return tuple(self.selection_history)


__all__ = [
    "NameSelectionManager",
]
