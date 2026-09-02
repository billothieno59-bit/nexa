"""
NEXA Canonical Architecture - Interface Layer (JARVIS)
File: core/interface/jarvis/conversation/session.py
Description: Tracks, records, and evaluates active interface conversational session histories.
"""

from typing import List, Dict, Any
import time


class ConversationSession:
    """Orchestrates runtime dialogue tracking configurations for single context interaction lifecycles."""

    def __init__(self, session_id: str, language_code: str = "sw-KE"):
        self.session_id = session_id
        self.primary_language = language_code
        self.history: List[Dict[str, Any]] = []
        self.start_timestamp: float = time.time()
        self._is_active: bool = True

    def record_dialogue_turn(self, role: str, message_text: str) -> Dict[str, Any]:
        """Appends a verified chat exchange turn frame structure onto the running local memory stack."""
        if not message_text.strip():
            raise ValueError("Turn message text payloads cannot be whitespace strings.")

        turn_payload = {"role": role, "text": message_text.strip(), "timestamp": time.time()}
        self.history.append(turn_payload)
        return turn_payload

    def close_active_session(self) -> Dict[str, Any]:
        """Locks the active status state flags to close conversational sequences safely."""
        self._is_active = False
        return {
            "session_id": self.session_id,
            "total_turns": len(self.history),
            "session_duration_sec": round(time.time() - self.start_timestamp, 2),
            "status": "archived",
        }

    @property
    def is_active(self) -> bool:
        """Indicates if the user-facing presentation loop session remains open."""
        return self._is_active
