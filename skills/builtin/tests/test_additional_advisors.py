"""
NEXA Builtin Skill Tests: additional builtin advisors
"""

from skills.registry.authorization import SkillAuthorizationGate
from skills.registry.registry import SkillRegistry
from skills.builtin.climate_advisor import register_builtin_skills as register_climate
from skills.builtin.health_advisor import register_builtin_skills as register_health
from skills.builtin.travel_advisor import register_builtin_skills as register_travel


def make_registry():
    registry = SkillRegistry()
    register_climate(registry)
    register_health(registry)
    register_travel(registry)
    return registry


def test_climate_topic_returns_guidance():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("environment.climate_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="drought")
    assert result["status"] == "found"
    assert "summary" in result["guidance"]


def test_health_topic_returns_guidance():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("health.primary_care_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="fever")
    assert result["status"] == "found"
    assert "summary" in result["guidance"]


def test_travel_topic_returns_guidance():
    registry = make_registry()
    gate = SkillAuthorizationGate(registry)
    handler = gate.get_authorized_handler("travel.route_advisor", frozenset({"TEXT.PROCESS"}))

    result = handler(topic="rain")
    assert result["status"] == "found"
    assert "summary" in result["guidance"]
