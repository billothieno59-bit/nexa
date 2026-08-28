"""
NEXA Africa Operating System
File: skills/registry/bootstrap.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Populates the canonical global_skill_registry with all
             builtin and privileged skills. Import this module (or
             global_skill_registry from here) to get a registry that is
             actually populated.
"""

from __future__ import annotations

from skills.registry.registry import global_skill_registry
import skills.builtin.accessibility_simplify as accessibility_simplify
import skills.builtin.accessibility_screen_reader as accessibility_screen_reader
import skills.builtin.perception_capture as perception_capture
import skills.builtin.knowledge_remember as knowledge_remember
import skills.builtin.knowledge_recall as knowledge_recall
import skills.builtin.agriculture_advisor as agriculture_advisor
import skills.builtin.construction_advisor as construction_advisor
import skills.builtin.electrical_advisor as electrical_advisor
import skills.builtin.solar_advisor as solar_advisor
import skills.builtin.water_systems_advisor as water_systems_advisor
import skills.builtin.livestock_advisor as livestock_advisor
import skills.builtin.education_advisor as education_advisor
import skills.builtin.workforce_advisor as workforce_advisor
import skills.builtin.entrepreneurship_advisor as entrepreneurship_advisor
import skills.privileged.system_shutdown as system_shutdown
import skills.privileged.ai_reasoning as ai_reasoning
import skills.privileged.image_generation as image_generation
import skills.privileged.voice_generation as voice_generation


def _bootstrap() -> None:
    accessibility_simplify.register_builtin_skills(global_skill_registry)
    accessibility_screen_reader.register_builtin_skills(global_skill_registry)
    perception_capture.register_builtin_skills(global_skill_registry)
    knowledge_remember.register_builtin_skills(global_skill_registry)
    knowledge_recall.register_builtin_skills(global_skill_registry)
    agriculture_advisor.register_builtin_skills(global_skill_registry)
    construction_advisor.register_builtin_skills(global_skill_registry)
    electrical_advisor.register_builtin_skills(global_skill_registry)
    solar_advisor.register_builtin_skills(global_skill_registry)
    water_systems_advisor.register_builtin_skills(global_skill_registry)
    livestock_advisor.register_builtin_skills(global_skill_registry)
    education_advisor.register_builtin_skills(global_skill_registry)
    workforce_advisor.register_builtin_skills(global_skill_registry)
    entrepreneurship_advisor.register_builtin_skills(global_skill_registry)
    system_shutdown.register_privileged_skills(global_skill_registry)
    ai_reasoning.register_privileged_skills(global_skill_registry)
    image_generation.register_privileged_skills(global_skill_registry)
    voice_generation.register_privileged_skills(global_skill_registry)


_bootstrap()


__all__ = [
    "global_skill_registry",
]
