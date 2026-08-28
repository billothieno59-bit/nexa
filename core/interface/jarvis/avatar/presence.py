"""
NEXA Canonical Architecture - Interface Layer (JARVIS)
File: core/interface/jarvis/avatar/presence.py
Description: Governs real-time visual avatar state metrics and expression profile configurations.
"""

from typing import Dict, Any


class AvatarPresenceEngine:
    """Manages visual animation rendering parameters and interactive posture profiles."""

    def __init__(self, visual_profile: str = "default_avatar"):
        self.profile = visual_profile
        self.current_state: str = "ambient_idle"
        self.blendshape_weights: Dict[str, float] = {
            "neutral": 1.0,
            "smile": 0.0,
            "talking": 0.0,
            "attentive_listening": 0.0
        }

    def transitional_state_update(self, structural_event: str) -> Dict[str, Any]:
        """Calculates weight targets based on immediate interactive interface changes."""
        cleaned_event = structural_event.lower().strip()

        if cleaned_event == "user_speaking":
            self.current_state = "listening"
            self.blendshape_weights = {"neutral": 0.3, "smile": 0.0, "talking": 0.0, "attentive_listening": 1.0}
        elif cleaned_event == "assistant_speaking":
            self.current_state = "speaking"
            self.blendshape_weights = {"neutral": 0.4, "smile": 0.2, "talking": 0.8, "attentive_listening": 0.0}
        else:
            self.current_state = "ambient_idle"
            self.blendshape_weights = {"neutral": 1.0, "smile": 0.0, "talking": 0.0, "attentive_listening": 0.0}

        return {
            "engine_state": self.current_state,
            "active_weights": self.blendshape_weights
        }
