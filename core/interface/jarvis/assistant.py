"""
NEXA Canonical Architecture - Interface Layer (JARVIS)
File: core/interface/jarvis/assistant.py
Description: The primary orchestrator that coordinates voice, session, avatar, and UI layers.
"""

from typing import Dict, Any
from core.interface.jarvis.identity.assistant_name import default_identity
from core.interface.jarvis.voice.input.stream_manager import VoiceStreamManager
from core.interface.jarvis.voice.output.audio_synthesizer import AudioSynthesizerEngine
from core.interface.jarvis.conversation.session import ConversationSession
from core.interface.jarvis.avatar.presence import AvatarPresenceEngine
from core.interface.jarvis.conversational_ui.layout import ConversationalUIRenderer


class JarvisInterfaceAssistant:
    """Central structural coordinator for public-facing interactive interface lifecycles."""

    def __init__(self, session_id: str):
        self.identity = default_identity
        self.voice_input = VoiceStreamManager()
        self.voice_output = AudioSynthesizerEngine()
        self.session = ConversationSession(session_id)
        self.avatar = AvatarPresenceEngine()
        self.ui = ConversationalUIRenderer()
        self._initialized: bool = True

    def process_incoming_user_interaction(self, input_text: str) -> Dict[str, Any]:
        """Orchestrates an active multi-turn interface step loop cleanly across all presentation components."""
        # 1. Update session ledger turn states
        self.session.record_dialogue_turn("user", input_text)

        # 2. Update physical animation visages for listening/processing postures
        self.avatar.transitional_state_update("user_speaking")

        # Simulated deep engine dispatch placeholder summary
        simulated_response = f"Habari! Nimepokea ujumbe wako: {input_text}"

        # 3. Log assistant turn details into session memory tracking
        self.session.record_dialogue_turn("assistant", simulated_response)

        # 4. Advance avatar to speaker layout postures
        avatar_render = self.avatar.transitional_state_update("assistant_speaking")

        # 5. Format display strings through the UI rendering module
        ui_display_string = self.ui.format_assistant_output(self.identity.assigned_name, simulated_response)

        # 6. Render the audio byte stream pipeline metrics
        audio_payload = self.voice_output.convert_text_to_audio_bytes(simulated_response)

        return {
            "status": "processed",
            "ui_text": ui_display_string,
            "avatar_state": avatar_render["engine_state"],
            "audio_bytes_generated": audio_payload["buffer_length_bytes"]
        }
