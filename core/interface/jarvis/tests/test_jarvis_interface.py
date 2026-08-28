"""
NEXA Africa Operating System
File: core/interface/jarvis/tests/test_jarvis_interface.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Unit tests for the JARVIS presentation layer, voice modules, and orchestrator hooks.
"""

from core.interface.jarvis.identity.assistant_name import default_identity
from core.interface.jarvis.identity.name_selection import NameSelectionManager
from core.interface.jarvis.voice.input.stream_manager import VoiceStreamManager
from core.interface.jarvis.assistant import JarvisInterfaceAssistant


def test_assistant_default_identity() -> None:
    """Verifies that the presentation layer defaults to the canonical JARVIS identity signature."""
    assert default_identity.assigned_name == "JARVIS"


def test_dynamic_name_selection_hook() -> None:
    """Verifies that the interface can be customized dynamically while enforcing safety length constraints."""
    manager = NameSelectionManager()

    # Valid structural name update
    update_result = manager.set_custom_name("Nexa Assistant")
    assert update_result["success"] is True
    assert default_identity.assigned_name == "Nexa Assistant"

    # Invalid length bound constraint enforcement
    invalid_result = manager.set_custom_name("X")
    assert invalid_result["success"] is False
    assert invalid_result["error"] is not None

    # Clean reset back to canonical base invariants
    reset_name = manager.reset_to_default()
    assert reset_name == "JARVIS"
    assert default_identity.assigned_name == "JARVIS"


def test_voice_stream_initialization() -> None:
    """Verifies that the audio input stream manager allocates proper capture device abstractions."""
    stream_manager = VoiceStreamManager(sample_rate=16000, channels=1)
    device_status = stream_manager.initialize_capture_device()

    assert device_status["status"] == "ready"
    assert device_status["sample_rate_hz"] == 16000
    assert device_status["channels_allocated"] == 1
    assert stream_manager.streaming_active is False


def test_integrated_assistant_processing_loop() -> None:
    """Verifies that the primary interface orchestrator cycles interaction turns deterministically."""
    assistant = JarvisInterfaceAssistant(session_id="test_runtime_session_101")
    interaction_payload = assistant.process_incoming_user_interaction("Rada nexa")

    assert interaction_payload["status"] == "processed"
    assert "ui_text" in interaction_payload
    assert interaction_payload["avatar_state"] == "speaking"
    assert interaction_payload["audio_bytes_generated"] > 0
    assert assistant.session.is_active is True
