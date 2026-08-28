"""
NEXA Canonical Architecture - Interface Layer (JARVIS)
File: core/interface/jarvis/wake_word.py
Description: Local background listener to track engine activation keyword phrases.
"""

from typing import Dict, Any


class WakeWordDetector:
    """Monitors incoming frame buffers for specific configured vocal activation tags."""

    def __init__(self, target_phrase: str = "nexa"):
        self.target_phrase = target_phrase.lower().strip()
        self._is_listening: bool = False

    def activate_detector(self) -> bool:
        """Starts background detection state flags safely."""
        self._is_listening = True
        return self._is_listening

    def deactivate_detector(self) -> bool:
        """Stops background detection state flags safely."""
        self._is_listening = False
        return self._is_listening

    def analyze_audio_chunk(self, matched_phrase_string: str) -> Dict[str, Any]:
        """Evaluates detected vocal patterns against the established engine activation phrase."""
        input_string = matched_phrase_string.lower().strip()
        is_triggered = (input_string == self.target_phrase)

        return {
            "detector_active": self._is_listening,
            "phrase_evaluated": input_string,
            "wake_word_triggered": is_triggered,
            "action_required": "signal_interface_loop" if is_triggered else "continue_background_listen"
        }
