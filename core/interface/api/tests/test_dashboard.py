from core.interface.api.dashboard import dashboard_status
from skills.registry.bootstrap import global_skill_registry


def test_dashboard_status_shape():
    result = dashboard_status()
    assert result["status"] == "online"
    assert result["system"] == "NEXA"
    assert "skills" in result
    assert "providers" in result


def test_dashboard_reports_real_skill_counts():
    result = dashboard_status()
    skills = result["skills"]

    skill_ids = global_skill_registry.list_skill_ids()
    manifests = [global_skill_registry.get_manifest(sid) for sid in skill_ids]
    expected_builtin = sum(1 for m in manifests if m.tier == "builtin")
    expected_privileged = sum(1 for m in manifests if m.tier == "privileged")

    assert skills["builtin"] == expected_builtin
    assert skills["privileged"] == expected_privileged
    assert skills["total"] == len(manifests)
    assert skills["total"] == skills["builtin"] + skills["privileged"]


def test_dashboard_reports_provider_keys():
    result = dashboard_status()
    providers = result["providers"]
    assert "anthropic" in providers
    assert "openai" in providers
    assert "elevenlabs" in providers
    for status in providers.values():
        assert status in ("connected", "not_configured")
