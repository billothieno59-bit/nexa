from skills.registry.bootstrap import global_skill_registry
from core.applications.cli import (
    list_available_skills,
    skill_parameter_names,
    run_skill,
)


def test_list_available_skills_matches_real_registry():
    skills = list_available_skills()
    expected = set(global_skill_registry.list_skill_ids())

    assert set(skills) == expected
    assert len(skills) == len(set(skills))  # no duplicates
    assert "agriculture.crop_advisor" in skills
    assert "generation.voice" in skills


def test_skill_parameter_names_for_known_shape():
    params = skill_parameter_names("knowledge.recall_fact")
    assert "subject" in params
    assert "predicate" in params
    assert "max_depth" in params


def test_skill_parameter_names_unknown_skill_returns_empty():
    assert skill_parameter_names("nonexistent.skill") == ()


def test_run_skill_as_founder_reaches_authorized_execution():
    result = run_skill("knowledge.recall_fact", subject="nexa_cli_smoke_test")
    # Founder identity + SYSTEM intent should be authorized, not denied
    # or rate-limited — whatever knowledge.recall_fact itself returns
    # (found/not_found) proves the real pipeline was reached.
    assert result.status == "executed"


def test_run_skill_unknown_caller_is_denied():
    result = run_skill(
        "knowledge.recall_fact",
        caller_id="unregistered_stranger",
        subject="nexa",
    )
    assert result.status == "denied"
