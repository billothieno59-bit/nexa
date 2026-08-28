"""
NEXA Africa Operating System
File: core/semantic/parser/usl_mapper.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Normalizes multi-lingual, code-switching strings into universal semantic representation tokens.
"""

from typing import Dict, Any


class UniversalSemanticLayerMapper:
    """Transforms regularized syntax text models into language-agnostic intent schema payloads."""

    def __init__(self) -> None:
        self.supported_intent_tokens: Dict[str, str] = {
            "hali gani": "INTENT_SYSTEM_DIAGNOSTIC_CHECK",
            "habari gani": "INTENT_SYSTEM_DIAGNOSTIC_CHECK",
            "mipango": "INTENT_PLANNING_ORCHESTRATION_GET",
            "pesa": "INTENT_RESOURCE_VALUE_TRANSACT",
            "kazi": "INTENT_PROCESS_EXECUTION_RUN",
            "viatu": "INTENT_IDENTITY_ASSET_QUERY"
        }

    def generate_universal_semantic_token(self, normalized_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Bridges normalized language varieties directly to invariant USL contract representations."""
        target_text: str = normalized_payload.get("normalized_swahili_target", "").lower().strip()
        resolved_intent: str = self.supported_intent_tokens.get(target_text, "INTENT_UNKNOWN_PASSTHROUGH")

        # Enforce strict fail-closed safety mechanics on unknown states
        is_executable: bool = resolved_intent != "INTENT_UNKNOWN_PASSTHROUGH"

        return {
            "usl_version": "1.0.0",
            "resolved_intent_token": resolved_intent,
            "origin_variety_source": normalized_payload.get("source_variety", "unknown_source"),
            "governed_execution_authorized": is_executable,
            "safety_status": "CLOSED" if not is_executable else "VERIFIED"
        }


# Global immutable schema mapper instance tracking
global_usl_mapper = UniversalSemanticLayerMapper()
