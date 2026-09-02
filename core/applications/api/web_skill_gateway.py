"""
NEXA Africa Operating System
File: core/applications/api/web_skill_gateway.py
Constitutional Owner: Bill Odhiambo Othieno
Description: The ONLY path by which core/applications/api/http_server.py
             may execute a skill. Deliberately narrow:

             - Registers a single fixed identity, WEB_CLIENT_ID, with
               role INTERFACE_NODE — never CONSTITUTIONAL_FOUNDER. This
               means privileged skills (generation.voice,
               generation.image, ai.reason, system.shutdown_nexa) are
               NEVER reachable from the web, because INTERFACE_NODE
               does not have their required permissions
               (see skills/registry/trust_bridge.py's ROLE_PERMISSIONS).
             - Explicitly rejects any skill whose manifest.tier is not
               "builtin", as a second, redundant layer of defense on
               top of the permission check above.
             - Goes through invoke_skill() — the exact same governed
               path (rate limiting, trust session, authorization) used
               by the CLI and every other caller. No shortcut.
"""

from __future__ import annotations

from typing import Any, Dict

from core.identity.profile.identity_manager import global_identity_manager
from skills.registry.bootstrap import global_skill_registry
from skills.registry.execution_bridge import SkillExecutionResult, invoke_skill

WEB_CLIENT_ID = "web_client_001"
WEB_CLIENT_ROLE = "INTERFACE_NODE"
WEB_REQUEST_INTENT = "TEXT.PROCESS"  # deliberately excludes "SYSTEM"


def _ensure_web_client_registered() -> None:
    """
    Registers the fixed web client identity once. Safe to call
    repeatedly — re-registration just overwrites the same profile with
    the same values.
    """
    global_identity_manager.register_identity_profile(
        identity_id=WEB_CLIENT_ID,
        role_tag=WEB_CLIENT_ROLE,
        display_alias="NEXA Web Client",
        is_governed=True,
    )


_ensure_web_client_registered()


def run_web_skill(skill_id: str, **kwargs: Any) -> SkillExecutionResult:
    """
    Execute a skill on behalf of the web client, only if it is a
    builtin (non-privileged) skill. Privileged skills are denied here
    before ever reaching invoke_skill(), as a defense-in-depth layer
    separate from the permission system itself.
    """
    manifest = global_skill_registry.get_manifest(skill_id)

    if manifest is None:
        return SkillExecutionResult(
            status="denied",
            skill_id=skill_id,
            message=f"Unknown skill_id: '{skill_id}'.",
        )

    if manifest.tier != "builtin":
        return SkillExecutionResult(
            status="denied",
            skill_id=skill_id,
            message="Only builtin skills are reachable from the web client.",
        )

    return invoke_skill(
        caller_id=WEB_CLIENT_ID,
        skill_id=skill_id,
        requested_intent=WEB_REQUEST_INTENT,
        **kwargs,
    )


def list_web_reachable_skills() -> Dict[str, Any]:
    """
    Return only builtin skill_ids and their parameter shape — never
    privileged ones — so the frontend can build a picker without
    exposing anything it can't actually call.
    """
    reachable = {}
    for skill_id in sorted(global_skill_registry.list_skill_ids()):
        manifest = global_skill_registry.get_manifest(skill_id)
        if manifest is not None and manifest.tier == "builtin":
            reachable[skill_id] = manifest.description
    return reachable


__all__ = [
    "WEB_CLIENT_ID",
    "run_web_skill",
    "list_web_reachable_skills",
]
