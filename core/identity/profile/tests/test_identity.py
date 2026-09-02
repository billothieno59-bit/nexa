"""
NEXA Africa Operating System
File: core/identity/profile/tests/test_identity.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Unit tests verifying deterministic identity profile validation boundaries.
"""

from core.identity.profile.identity_manager import global_identity_manager


def test_founder_identity_bootstrap_record() -> None:
    """Verifies that the supreme constitutional steward profile registers accurately during booting steps."""
    check_report = global_identity_manager.validate_access_rights("founder_root_001", "CONSTITUTIONAL_FOUNDER")
    assert check_report["authorized"] is True
    assert check_report["matched_alias"] == "Bill Odhiambo Othieno"
    assert check_report["auth_status"] == "VERIFIED"


def test_custom_profile_registration_and_validation() -> None:
    """Verifies dynamic addition of peripheral operator profiles under strict access controls."""
    global_identity_manager.register_identity_profile(
        identity_id="operator_test_99", role_tag="INTERFACE_NODE", display_alias="Jarvis Client Link", is_governed=True
    )

    success_check = global_identity_manager.validate_access_rights("operator_test_99", "INTERFACE_NODE")
    assert success_check["authorized"] is True
    assert success_check["execution_clearance"] is True

    failed_check = global_identity_manager.validate_access_rights("operator_test_99", "SYSTEM_ROOT_ADMIN")
    assert failed_check["authorized"] is False
    assert failed_check["auth_status"] == "CLOSED"


def test_unregistered_caller_fails_closed() -> None:
    """Ensures unknown identifier validation queries fail closed explicitly by default."""
    blind_query = global_identity_manager.validate_access_rights("malicious_unregistered_node", "ANY_ROLE")
    assert blind_query["authorized"] is False
    assert blind_query["auth_status"] == "CLOSED"
    assert blind_query["execution_clearance"] is False
