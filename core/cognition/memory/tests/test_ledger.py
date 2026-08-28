"""
NEXA Africa Operating System
File: core/cognition/memory/tests/test_ledger.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Unit tests verifying deterministic session ledger serialization boundaries.
"""

import json
from core.cognition.memory.ledger_manager import global_session_ledger


def test_session_ledger_state_commit() -> None:
    """Verifies that conversation frames commit deterministically without operational side effects."""
    mock_history = [
        {"role": "user", "text": "Rada nexa", "timestamp": 1787247200.0},
        {"role": "assistant", "text": "Hali gani! Nimepokea ujumbe.", "timestamp": 1787247201.0}
    ]

    commit_report = global_session_ledger.commit_session_state("sess_test_u2", mock_history)
    assert commit_report["session_id"] == "sess_test_u2"
    assert commit_report["total_frames_committed"] == 2
    assert commit_report["checkpoint_persisted"] is True


def test_session_ledger_extraction_pipeline() -> None:
    """Verifies retrieval and validates integrity formats for compiled ledger tracking data strings."""
    mock_history = [{"role": "user", "text": "Form leo?", "timestamp": 1787247300.0}]
    global_session_ledger.commit_session_state("sess_test_u3", mock_history)

    json_string = global_session_ledger.fetch_serialized_ledger("sess_test_u3")
    assert json_string is not None

    parsed_data = json.loads(json_string)
    assert len(parsed_data) == 1
    assert parsed_data[0]["text"] == "Form leo?"


def test_unregistered_ledger_returns_none() -> None:
    """Ensures unknown or missing history queries fail gracefully by returning isolated null outputs."""
    missing_ledger = global_session_ledger.fetch_serialized_ledger("non_existent_session_id")
    assert missing_ledger is None
