"""
NEXA Africa Operating System
File: core/services/config/validator.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Validates NEXA's runtime configuration at startup, per
             ENGINEERING_RULES.md rule 8. Reports what is missing or
             invalid rather than allowing silent partial operation.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List

from core.governance.trust.shutdown.key_guard import EMERGENCY_KEY_ENV_VAR


@dataclass(frozen=True)
class ConfigValidationReport:
    """
    Result of a configuration validation pass.
    """

    valid: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def validate_startup_configuration() -> ConfigValidationReport:
    """
    Check known configuration requirements. Missing optional-but-
    important config becomes a warning; missing required config becomes
    an error. This does not raise or exit itself — the caller decides
    what to do with the report, but a report with errors should
    generally block unsafe startup.
    """
    warnings: List[str] = []
    errors: List[str] = []

    if not os.environ.get(EMERGENCY_KEY_ENV_VAR):
        warnings.append(
            f"{EMERGENCY_KEY_ENV_VAR} is not set. The emergency shutdown "
            "capability will fail closed (deny all requests) until it is configured."
        )

    valid = len(errors) == 0

    return ConfigValidationReport(valid=valid, warnings=warnings, errors=errors)


__all__ = [
    "ConfigValidationReport",
    "validate_startup_configuration",
]
