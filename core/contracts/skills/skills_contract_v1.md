# NEXA Skills Registry Contract v1

## Status

Draft — foundational scope only. This contract precedes implementation,
per CONSTITUTION.md Principle 4.

## Purpose

Defines how a "skill" (a discrete capability NEXA can offer — builtin,
community, enterprise, or privileged) declares itself, including the
permissions it requires, and defines the enforcement gate that must be
passed before a skill's handler can ever be retrieved for use.

## Canonical location

`skills/registry/`

## Naming note

An earlier proposal suggested calling a permission-definition module
"UPL" (Universal Permission Language). That collides with the already-
canonical UPL = Universal Perception Layer (`core/perception/`, built).
This contract does not use that name. Skills declare required
permissions as plain, namespaced strings (e.g. "KERNEL.MANAGE").

## Responsibilities

- `SkillManifest` describes a skill: id, name, description, tier, and
  the permission strings it requires.
- `SkillRegistry` stores manifests and handler callables, keyed by
  skill_id. It never invokes a handler and never authorizes anything.
- `SkillAuthorizationGate` is the ONLY sanctioned way to retrieve a
  skill's handler for actual use. It checks a caller's granted
  permissions against the skill's declared required_permissions and
  fails closed — denying access — if any required permission is
  missing, if the skill is unknown, or if no granted permissions are
  provided.

## What this must NOT do

- `SkillRegistry.get_handler()` remains a raw introspection method (used
  by tests and diagnostics) and must never be treated as safe for actual
  invocation — `SkillAuthorizationGate.get_authorized_handler()` is the
  only method that should be used to obtain a handler meant to run.
- Must not execute a skill's handler itself. Real invocation, if wired
  in later, must still go through the governed execution pipeline
  (Decision -> Planner -> Orchestrator -> Dispatcher -> Authorization ->
  Executor).
- Must not invent what a permission string means. The gate only checks
  string membership; deciding what set of permissions a given caller or
  session is granted is a separate concern (future integration with
  `core/execution/authorization/policy.py` and identity/trust), not
  implemented by this contract.

## Core data contract

`SkillManifest`:
- `skill_id: str`
- `name: str`
- `description: str`
- `tier: str` — one of "builtin", "community", "enterprise", "privileged"
- `required_permissions: Tuple[str, ...]`

## Versioning

Wiring `SkillAuthorizationGate` to a real, session-based source of
granted permissions (rather than a caller-supplied set, as built here)
requires a new contract version once that integration is designed.