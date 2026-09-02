"""
NEXA Africa Operating System
File: core/interaction/communication/registry/language_registry.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Core registry to document and track active language profile specifications.
"""

from typing import Dict, Any, List


class LanguageRegistry:
    """Manages system language variants, accommodating low-resource formats and local dialects."""

    def __init__(self) -> None:
        self._registered_variants: Dict[str, Dict[str, Any]] = {}
        self._bootstrap_default_profiles()

    def _bootstrap_default_profiles(self) -> None:
        """Initializes the baseline structural settings for African-first language operations."""
        self.register_variant(variant_id="sw_KE", display_name="Standard Swahili", is_low_resource=False)
        self.register_variant(variant_id="sheng_variety", display_name="Sheng Language Variety", is_low_resource=True)

    def register_variant(self, variant_id: str, display_name: str, is_low_resource: bool) -> None:
        """Saves a new explicit language format standard blueprint profile configuration."""
        self._registered_variants[variant_id] = {
            "display_name": display_name,
            "is_low_resource": is_low_resource,
            "status": "active",
        }

    def fetch_active_variants(self) -> List[str]:
        """Returns lists matching code references for all registered language definitions."""
        return list(self._registered_variants.keys())


# Global standard platform profile registry configuration template instantiation
global_language_registry = LanguageRegistry()
