import pytest

from core.governance.trust.voice_identity import VoicePassphraseRegistry


@pytest.fixture
def registry():
    return VoicePassphraseRegistry(salt="test_salt")


def test_enroll_then_confirm_matching_passphrase_succeeds(registry):
    registry.enroll("bill", "the mint orb glows at dawn")
    result = registry.confirm("bill", "the mint orb glows at dawn")

    assert result.confirmed is True
    assert result.identity_id == "bill"


def test_confirm_is_case_and_whitespace_insensitive(registry):
    registry.enroll("bill", "the mint orb glows at dawn")
    result = registry.confirm("bill", "  THE Mint Orb Glows At Dawn  ")

    assert result.confirmed is True


def test_confirm_wrong_passphrase_fails_closed(registry):
    registry.enroll("bill", "the mint orb glows at dawn")
    result = registry.confirm("bill", "wrong phrase entirely")

    assert result.confirmed is False
    assert result.reason == "Passphrase did not match."


def test_confirm_unenrolled_identity_fails_closed(registry):
    result = registry.confirm("stranger", "anything at all")

    assert result.confirmed is False
    assert result.reason == "No passphrase enrolled for this identity."


def test_confirm_empty_spoken_text_fails_closed(registry):
    registry.enroll("bill", "the mint orb glows at dawn")
    result = registry.confirm("bill", "")

    assert result.confirmed is False
    assert result.reason == "Empty or invalid spoken text."


def test_enroll_rejects_empty_identity_id(registry):
    with pytest.raises(ValueError):
        registry.enroll("", "some passphrase")


def test_enroll_rejects_empty_passphrase(registry):
    with pytest.raises(ValueError):
        registry.enroll("bill", "")


def test_is_enrolled_reports_correctly(registry):
    assert registry.is_enrolled("bill") is False
    registry.enroll("bill", "the mint orb glows at dawn")
    assert registry.is_enrolled("bill") is True


def test_plaintext_passphrase_is_never_stored(registry):
    registry.enroll("bill", "the mint orb glows at dawn")
    stored_hash = registry._passphrase_hashes["bill"]

    assert "the mint orb glows at dawn" not in stored_hash
    assert len(stored_hash) == 64  # sha256 hex digest length