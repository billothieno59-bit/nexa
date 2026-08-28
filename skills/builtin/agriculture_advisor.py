"""
NEXA Africa Operating System
File: skills/builtin/agriculture_advisor.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Builtin skill providing general planting-season guidance for
             common East African staple crops, from a small curated
             reference table. This is general guidance, not a substitute
             for local agricultural extension services — the response
             says so explicitly. Data is static and human-curated, not
             generated, since incorrect agricultural advice can cause
             real harm to someone's crop and livelihood.
"""

from __future__ import annotations

from typing import Any, Dict

from skills.registry.manifest import SkillManifest
from skills.registry.registry import SkillRegistry

AGRICULTURE_ADVISOR_SKILL = SkillManifest(
    skill_id="agriculture.crop_advisor",
    name="Crop Planting Advisor",
    description="Provides general planting-season guidance for common staple crops.",
    tier="builtin",
    required_permissions=("TEXT.PROCESS",),
)

# Static, curated reference data. General guidance only — actual planting
# timing varies by specific location, elevation, and year-to-year rainfall.
_CROP_GUIDANCE: Dict[str, Dict[str, Any]] = {
    "maize": {
        "common_names": ["maize", "corn"],
        "typical_planting_season": (
            "Start of the long rains (varies by region; "
            "commonly March-May in much of East Africa)"
        ),
        "typical_days_to_maturity": "90-150 days depending on variety",
        "notes": "Prefers well-drained soil; avoid waterlogged fields.",
    },
    "beans": {
        "common_names": ["beans", "common bean"],
        "typical_planting_season": "Can be planted in both long and short rains seasons",
        "typical_days_to_maturity": "60-90 days",
        "notes": "Often intercropped with maize; fixes nitrogen in soil.",
    },
    "sorghum": {
        "common_names": ["sorghum"],
        "typical_planting_season": "Start of rains; more drought-tolerant than maize",
        "typical_days_to_maturity": "100-140 days depending on variety",
        "notes": "Good choice for drier regions with less reliable rainfall.",
    },
    "cassava": {
        "common_names": ["cassava", "manioc"],
        "typical_planting_season": "Can be planted at start of rains; tolerant of varied timing",
        "typical_days_to_maturity": "8-24 months depending on variety",
        "notes": "Very drought-tolerant once established; stores well in the ground.",
    },
}

_DISCLAIMER = (
    "This is general guidance only, not a substitute for advice from your "
    "local agricultural extension officer, who can account for your specific "
    "soil, elevation, and this season's rainfall forecast."
)


def _crop_advisor_handler(crop: str) -> Dict[str, Any]:
    normalized = crop.strip().lower()

    for key, info in _CROP_GUIDANCE.items():
        if normalized == key or normalized in info["common_names"]:
            return {
                "status": "found",
                "crop": key,
                "guidance": {
                    "typical_planting_season": info["typical_planting_season"],
                    "typical_days_to_maturity": info["typical_days_to_maturity"],
                    "notes": info["notes"],
                },
                "disclaimer": _DISCLAIMER,
            }

    return {
        "status": "not_found",
        "crop": crop,
        "available_crops": list(_CROP_GUIDANCE.keys()),
        "disclaimer": _DISCLAIMER,
    }


def register_builtin_skills(registry: SkillRegistry) -> None:
    registry.register(AGRICULTURE_ADVISOR_SKILL, _crop_advisor_handler)


__all__ = [
    "AGRICULTURE_ADVISOR_SKILL",
    "register_builtin_skills",
]
