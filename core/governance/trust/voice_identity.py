"""
NEXA Africa Operating System
File: core/governance/trust/voice_identity.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Confirms WHO is speaking via a spoken passphrase — separate
             from core/semantic/parser/voice_command_bridge.py, which
             resolves WHAT to do. Stores only a salted hash of each
             identity's passphrase, never the plaintext, and never logs
             the plaintext either. Fails closed: no enrolled passphrase,
             an empty spoken text, or a mismatch all deny confirmation.
"""

from __future__ import annotations

import hashlib
import hmac
import os
from dataclasses import dataclass
from typing import Dict, Optional

from core.services.logging.logger import get_logger

logger = get_logger(__name__)

SALT_ENV_VAR = "NEXA_VOICE_IDENTITY_SALT"
DEFAULT_SALT = "NEXA_VOICE_SALT_V1"


def _hash_passphrase(passphrase: str, salt: str) -> str:
    normalized = passphrase.strip().lower()
    return hashlib.sha256(f"{salt}:{normalized}".encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class VoiceIdentityResult:
    """
    Result of a spoken-passphrase identity confirmation attempt. The
    rest of the system should reason only about this — never the raw
    passphrase or its hash.
    """

    confirmed: bool
    identity_id: str
    reason: str


class VoicePassphraseRegistry:
    """
    Stores salted passphrase hashes per identity_id. Enrollment and
    confirmation are separate steps — enrolling is not itself a
    confirmation, and confirming without enrollment always fails
    closed.
    """

    def __init__(self, salt: Optional[str] = None) -> None:
        self._salt = salt or os.environ.get(SALT_ENV_VAR, DEFAULT_SALT)
        self._passphrase_hashes: Dict[str, str] = {}

    def enroll(self, identity_id: str, passphrase: str) -> None:
        if not isinstance(identity_id, str) or not identity_id.strip():
            raise ValueError("identity_id must be a non-empty string.")
        if not isinstance(passphrase, str) or not passphrase.strip():
            raise ValueError("passphrase must be a non-empty string.")

        self._passphrase_hashes[identity_id] = _hash_passphrase(passphrase, self._salt)
        logger.info("Voice passphrase enrolled for identity_id=%s", identity_id)

    def is_enrolled(self, identity_id: str) -> bool:
        return identity_id in self._passphrase_hashes

    def confirm(self, identity_id: str, spoken_text: str) -> VoiceIdentityResult:
        """
        Confirm whether spoken_text matches the enrolled passphrase for
        identity_id. Never raises on bad input — always returns a
        VoiceIdentityResult, fail-closed.
        """
        if not isinstance(spoken_text, str) or not spoken_text.strip():
            return VoiceIdentityResult(
                confirmed=False,
                identity_id=identity_id,
                reason="Empty or invalid spoken text.",
            )

        expected_hash = self._passphrase_hashes.get(identity_id)

        if expected_hash is None:
            return VoiceIdentityResult(
                confirmed=False,
                identity_id=identity_id,
                reason="No passphrase enrolled for this identity.",
            )

        provided_hash = _hash_passphrase(spoken_text, self._salt)
        matched = hmac.compare_digest(expected_hash, provided_hash)

        if matched:
            logger.info("Voice identity confirmed for identity_id=%s", identity_id)
        else:
            logger.warning("Voice identity confirmation failed for identity_id=%s", identity_id)

        return VoiceIdentityResult(
            confirmed=matched,
            identity_id=identity_id,
            reason="Passphrase matched." if matched else "Passphrase did not match.",
        )


global_voice_identity_registry = VoicePassphraseRegistry()


__all__ = [
    "VoiceIdentityResult",
    "VoicePassphraseRegistry",
    "global_voice_identity_registry",
]