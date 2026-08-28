"""
NEXA Skills Bootstrap Tests.
"""

from skills.registry.bootstrap import global_skill_registry

_ALL_BUILTIN_IDS = (
    "accessibility.simplify_text",
    "accessibility.format_screen_reader",
    "perception.capture_text",
    "knowledge.remember_fact",
    "knowledge.recall_fact",
    "agriculture.crop_advisor",
    "construction.reference_advisor",
    "electrical.reference_advisor",
    "solar.reference_advisor",
    "water_systems.reference_advisor",
    "livestock.reference_advisor",
    "education.study_advisor",
    "workforce.reference_advisor",
    "entrepreneurship.reference_advisor",
)

_ALL_PRIVILEGED_IDS = (
    "system.shutdown_nexa",
    "ai.reason",
    "generation.image",
    "generation.voice",
)


def test_global_registry_has_all_builtin_and_privileged_skills():
    ids = global_skill_registry.list_skill_ids()
    for skill_id in _ALL_BUILTIN_IDS + _ALL_PRIVILEGED_IDS:
        assert skill_id in ids


def test_privileged_skills_are_privileged_tier():
    for skill_id in _ALL_PRIVILEGED_IDS:
        manifest = global_skill_registry.get_manifest(skill_id)
        assert manifest.tier == "privileged"


def test_builtin_skills_remain_builtin_tier():
    for skill_id in _ALL_BUILTIN_IDS:
        manifest = global_skill_registry.get_manifest(skill_id)
        assert manifest.tier == "builtin"
