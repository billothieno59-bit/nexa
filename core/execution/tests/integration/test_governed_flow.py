"""
NEXA Africa Operating System
File: core/execution/tests/integration/test_governed_flow.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Full-stack integration test verifying deterministic, multi-layered governed execution flow.
"""

from core.governance.trust.signature.guard_engine import global_trust_guard
from core.interaction.communication.adapters.sheng_adapter import default_sheng_adapter
from core.semantic.parser.usl_mapper import global_usl_mapper
from core.execution.executor.bootstrap import get_handler_registry


def test_full_governed_execution_lifecycle_success() -> None:
    """Verifies complete deterministic pipeline flow from a raw modern Sheng token to a resolved handler."""
    # 1. Simulate an interaction input payload coming from the interface boundary
    raw_input_token = "ganji"

    # 2. Universal Communication Layer (UCL) Adapter Normalization
    ucl_report = default_sheng_adapter.normalize_input_phrase(raw_input_token)
    assert ucl_report["normalized_swahili_target"] == "pesa"
    assert ucl_report["translation_applied"] is True

    # 3. Universal Semantic Layer (USL) Intent Invariant Mapping
    usl_report = global_usl_mapper.generate_universal_semantic_token(ucl_report)
    assert usl_report["resolved_intent_token"] == "INTENT_RESOURCE_VALUE_TRANSACT"
    assert usl_report["governed_execution_authorized"] is True

    # 4. Universal Trust Layer (UTL) Invariant Cryptographic Validation
    contract_payload = usl_report["resolved_intent_token"]
    calculated_sig = global_trust_guard.generate_payload_signature(contract_payload)

    trust_report = global_trust_guard.verify_contract_integrity(contract_payload, calculated_sig)
    assert trust_report["verified"] is True
    assert trust_report["safety_status"] == "VERIFIED"

    # 5. Canonical handler registry resolution (resolve-only, never invoked)
    if trust_report["action_authorized"]:
        registry = get_handler_registry()
        handler = registry.get_handler(usl_report["resolved_intent_token"])
        assert handler is not None
    else:
        raise RuntimeError("Cryptographic authorization block failed unexpectedly.")


def test_corrupted_pipeline_fails_closed() -> None:
    """Ensures that any string layout changes mid-transit halt execution immediately to fail closed."""
    # 1. Normal workflow path up to the USL intent parsing layer
    ucl_report = default_sheng_adapter.normalize_input_phrase("mboka")
    usl_report = global_usl_mapper.generate_universal_semantic_token(ucl_report)
    assert usl_report["resolved_intent_token"] == "INTENT_PROCESS_EXECUTION_RUN"

    # 2. Generate a valid hash signature for the verified intent token
    valid_sig = global_trust_guard.generate_payload_signature(usl_report["resolved_intent_token"])

    # 3. Simulate a malicious or truncated payload text change before execution dispatch
    corrupted_intent_token = "INTENT_MALICIOUS_SIDE_EFFECT_INJECTION"

    # 4. Trust layer evaluates the block and forcefully fails closed
    trust_report = global_trust_guard.verify_contract_integrity(corrupted_intent_token, valid_sig)
    assert trust_report["verified"] is False
    assert trust_report["safety_status"] == "CLOSED"

    # 5. Canonical handler registry confirms authorization is denied before any resolution
    action_authorized = trust_report["action_authorized"]
    assert action_authorized is False
