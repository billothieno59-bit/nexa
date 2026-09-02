"""
NEXA Africa Operating System
File: core/applications/cli.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Interactive command-line entrypoint. Lists real registered
             skills (via skills.registry.bootstrap) and runs them
             through the actual governed pipeline — invoke_skill(),
             meaning rate limiting, trust session resolution, and
             SkillAuthorizationGate all apply exactly as they do
             everywhere else. Nothing here bypasses authorization.

             Runs as the bootstrapped founder identity (founder_root_001)
             by default, since this is a local interactive tool
             operated by the project owner — not a network-facing
             surface. requested_intent always includes "SYSTEM" so the
             founder role (and therefore every permission in
             ROLE_PERMISSIONS) is available, matching how a human
             operator at the machine is expected to have full access.
"""

from __future__ import annotations

import inspect
from typing import Any, Dict, Tuple

from skills.registry.bootstrap import global_skill_registry
from skills.registry.execution_bridge import SkillExecutionResult, invoke_skill

DEFAULT_CALLER_ID = "founder_root_001"
DEFAULT_INTENT = "SYSTEM.CLI_REQUEST"


def list_available_skills() -> Tuple[str, ...]:
    """
    Return every registered skill_id, sorted, for display or selection.
    """
    return tuple(sorted(global_skill_registry.list_skill_ids()))


def skill_parameter_names(skill_id: str) -> Tuple[str, ...]:
    """
    Introspect a skill's handler to find its parameter names, so the
    CLI can prompt for exactly what a skill needs without hardcoding
    per-skill argument lists. Does not execute the handler — get_handler()
    is read-only, same as registry.py's own docstring guarantees.
    """
    handler = global_skill_registry.get_handler(skill_id)
    if handler is None:
        return ()

    signature = inspect.signature(handler)
    return tuple(signature.parameters.keys())


def run_skill(
    skill_id: str,
    caller_id: str = DEFAULT_CALLER_ID,
    requested_intent: str = DEFAULT_INTENT,
    **kwargs: Any,
) -> SkillExecutionResult:
    """
    Run a skill through the real governed pipeline. This is the only
    execution path the CLI uses — no shortcut around invoke_skill().
    """
    return invoke_skill(
        caller_id=caller_id,
        skill_id=skill_id,
        requested_intent=requested_intent,
        **kwargs,
    )


def _prompt_for_kwargs(skill_id: str) -> Dict[str, Any]:
    param_names = skill_parameter_names(skill_id)
    kwargs: Dict[str, Any] = {}

    for name in param_names:
        raw = input(f"  {name} (press Enter to skip): ").strip()
        if raw:
            kwargs[name] = raw

    return kwargs


def main() -> None:
    print("NEXA — interactive command line.")
    print("Running as founder identity: " + DEFAULT_CALLER_ID)
    print("Type 'list' to see skills, a skill_id to run it, or 'quit' to exit.\n")

    while True:
        try:
            choice = input("nexa> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not choice:
            continue

        if choice in ("quit", "exit"):
            print("Exiting.")
            break

        if choice == "list":
            for skill_id in list_available_skills():
                print(f"  {skill_id}")
            continue

        if choice not in list_available_skills():
            print(f"Unknown skill_id: '{choice}'. Type 'list' to see valid options.")
            continue

        kwargs = _prompt_for_kwargs(choice)
        result = run_skill(choice, **kwargs)

        print(f"\nstatus: {result.status}")
        print(f"message: {result.message}")
        if result.result is not None:
            print(f"result: {result.result}")
        print()


if __name__ == "__main__":
    main()
