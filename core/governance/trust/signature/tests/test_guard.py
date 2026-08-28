"""
NEXA Africa Operating System
File: core/governance/trust/signature/tests/test_guard.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Unit tests verifying cryptographic signature boundaries inside the trust layer.
"""

from core.governance.trust.signature.guard_engine import global_trust_guard


def test_signature_deterministic_generation() -> None:
    """Verifies that identical string inputs generate matching hash payloads consistently."""
    test_content = "INTENT_SYSTEM_DIAGNOSTIC_CHECK"
    sig_1 = global_trust_guard.generate_payload_signature(test_content)
    sig_2 = global_trust_guard.generate_payload_signature(test_content)

    assert sig_1 == sig_2
    assert len(sig_1) == 64  # Standard SHA-256 string length character output


def test_contract_integrity_verification_success() -> None:
    """Verifies successful authorization when matching strings and signatures align perfectly."""
    payload = "NEXA_CORE_STATE_ALPHA_VALID"
    valid_sig = global_trust_guard.generate_payload_signature(payload)

    report = global_trust_guard.verify_contract_integrity(payload, valid_sig)
    assert report["verified"] is True
    assert report["safety_status"] == "VERIFIED"
    assert report["action_authorized"] is True


def test_corrupted_contract_fails_closed() -> None:
    """Ensures mismatched signatures or modified text data sets fail closed immediately."""
    payload = "NEXA_CORE_STATE_ALPHA_VALID"
    valid_sig = global_trust_guard.generate_payload_signature(payload)

    # Simulate a malicious or truncated payload text change
    corrupted_payload = "NEXA_CORE_STATE_ALPHA_MALICIOUS"

    report = global_trust_guard.verify_contract_integrity(corrupted_payload, valid_sig)
    assert report["verified"] is False
    assert report["safety_status"] == "CLOSED"
    assert report["action_authorized"] is False
