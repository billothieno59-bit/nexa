"""
NEXA Config Validator Tests.
"""

from core.services.config.validator import validate_startup_configuration


def test_missing_emergency_key_produces_warning_not_error(monkeypatch):
    monkeypatch.delenv("NEXA_EMERGENCY_KEY", raising=False)

    report = validate_startup_configuration()

    assert report.valid is True
    assert any("NEXA_EMERGENCY_KEY" in w for w in report.warnings)
    assert report.errors == []


def test_configured_emergency_key_produces_no_warning(monkeypatch):
    monkeypatch.setenv("NEXA_EMERGENCY_KEY", "some-real-key")

    report = validate_startup_configuration()

    assert not any("NEXA_EMERGENCY_KEY" in w for w in report.warnings)
