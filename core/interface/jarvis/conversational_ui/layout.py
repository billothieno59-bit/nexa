"""
NEXA Canonical Architecture - Interface Layer (JARVIS)
File: core/interface/jarvis/conversational_ui/layout.py
Description: Packages, renders, and structures visual text strings for display panels.
"""

from typing import Dict, Any


class ConversationalUIRenderer:
    """Manages string wrapping, layout borders, and prompt notification framing configurations."""

    def __init__(self, interface_width: int = 80):
        self.width = interface_width

    def format_assistant_output(self, sender_name: str, response_text: str) -> str:
        """Structures a clean text frame block for terminal console logs."""
        prefix = f"[{sender_name.upper()}]: "
        clean_text = response_text.strip()
        return f"{prefix}{clean_text}"

    def generate_system_notification(self, notification_title: str, severity: str = "INFO") -> Dict[str, Any]:
        """Creates formal interface banner alert templates for immediate event routing."""
        return {
            "component_target": "conversational_ui",
            "alert_type": severity.upper(),
            "headline": notification_title.strip().upper(),
            "border_padding_char": "=",
            "render_width": self.width,
        }
