"""
NEXA Canonical Architecture - Interface Layer (JARVIS)
File: core/interface/jarvis/voice/input/stream_manager.py
Description: Interfaces with local audio inputs to capture user voice activity streams.
"""

from typing import Dict, Any, Optional


class VoiceStreamManager:
    """Manages raw audio recording buffers and streams before transferring to perception processing."""

    def __init__(self, sample_rate: int = 16000, channels: int = 1):
        self.sample_rate = sample_rate
        self.channels = channels
        self._is_active: bool = False
        self._active_stream_id: Optional[str] = None

    def initialize_capture_device(self) -> Dict[str, Any]:
        """Verifies local system input status and locks audio context configuration specifications."""
        # Baseline abstraction representing physical micro-device capture locks
        self._active_stream_id = "stream_voice_dev_0"
        return {
            "status": "ready",
            "device_id": self._active_stream_id,
            "sample_rate_hz": self.sample_rate,
            "channels_allocated": self.channels
        }

    def begin_streaming(self) -> bool:
        """Enables internal active status state markers to start receiving voice buffers."""
        if not self._active_stream_id:
            self.initialize_capture_device()
        self._is_active = True
        return self._is_active

    def close_streaming(self) -> bool:
        """Gracefully disconnects audio streaming state frameworks safely."""
        self._is_active = False
        return self._is_active

    @property
    def streaming_active(self) -> bool:
        """Returns truth status indicators detailing system device recording states."""
        return self._is_active
