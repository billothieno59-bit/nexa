# NEXA Engineering Rules

Status: adopted. These rules govern every change to this codebase,
alongside CONSTITUTION.md (architecture) and SYSTEM_INSTRUCTION.md
(coding workflow). Where a rule here would require tooling that is not
yet wired into this repository, that is noted explicitly — a rule
documented but not yet enforced is still binding, but must not be
claimed as "enforced" until the tooling behind it actually runs clean.

## 1. Zero-regression rule

Every change must leave all existing tests passing, plus any new tests
the change requires. A change that knowingly reduces the passing test
count is rejected. Current baseline: verify via `python -m pytest`
before treating any change as complete — never assume a prior claimed
count is still accurate without re-running it.

## 2. No untested production code

New production logic requires tests covering both the expected
behavior and its failure modes (unauthorized input, malformed input,
unknown state). A change without a corresponding test is incomplete.

## 3. Fail-closed security

Unknown, invalid, missing, ambiguous, or unauthorized input is denied
by default. Only an explicitly validated and authorized path may
proceed. This is already the pattern used throughout
core/execution/, core/governance/trust/, and skills/registry/ — keep it.

## 4. Strict architectural boundaries

Requests flow through the governed pipeline (Decision -> Planner ->
Orchestrator -> Dispatcher -> Authorization -> Executor). No new module
may jump directly from input to execution, or from a user-facing layer
to a privileged one, bypassing this chain.

## 5. Identity is not authorization

Knowing who or what something is must never itself grant permission.
Identity resolution (core/governance/trust/session.py) and
authorization (core/execution/authorization/policy.py) are separate
modules; authorization consumes only a resolved set of granted roles,
never raw identity.

## 6. No hidden side effects

A function's effects should be visible from its signature and
docstring. Avoid functions that silently mutate persistent state,
execute commands, or contact external services without that being the
stated purpose of calling them.

## 7. Deterministic core where possible

Prefer isolating system time, randomness, environment variables, and
network calls behind a clear interface (e.g. `EmergencyKeyGuard` reads
`NEXA_EMERGENCY_KEY` in one place, not scattered across callers) so the
surrounding logic stays testable and predictable.

## 8. Configuration must be validated

Missing or invalid required configuration (e.g. an unset
`NEXA_EMERGENCY_KEY`) must fail closed at the point of use, not allow
partial or silently-degraded operation. This is already how
`EmergencyKeyGuard.is_configured()` behaves — keep that pattern.

## 9. No secrets in source

Never commit API keys, passwords, tokens, or credentials. Emergency
keys and API keys are read from environment variables
(`NEXA_EMERGENCY_KEY`), never hardcoded — this has already been fixed
once this project (the original API gateway had a hardcoded default
key; it does not anymore).

## 10. Dependency discipline

Every entry in requirements.txt/pyproject.toml dependencies should have
a clear reason to exist. Review new dependencies before adding them;
prefer the standard library when it's sufficient (e.g. `hmac`,
`secrets`, `sqlite3` are already used this way).

## 11. Type hints

Use explicit typing throughout, as already practiced in this codebase
(dataclasses with typed fields, typed function signatures). Full static
type-checking (e.g. mypy) is not yet wired into CI — see "Not yet
enforced" below.

## 12. Complexity limits

Keep functions and classes focused. If a function is doing several
distinct jobs (e.g. resolving identity AND checking authorization AND
executing), split it — this is the same reasoning behind separating
`resolve_trust_session()` from `authorize_identity_context()`.

## 13. Error handling

No bare `except: pass`. Catch specific exceptions, log them (via
`core/services/logging/`), and either fail closed or re-raise a clear,
specific error — see `SemanticRouter.dispatch()`'s `RouterHandlerError`
as the existing pattern to follow.

## 14. Logging and auditability

Security-relevant operations (authorization decisions, shutdown
attempts, skill authorization) must log what happened, without ever
logging secret values themselves (keys, tokens). This is already how
`EmergencyKeyGuard` and `SkillAuthorizationGate` behave.

## 15. No direct production mutation without authorization

State-changing operations must pass through validate -> authorize ->
execute -> audit, never request -> execute directly. This is the
existing execution pipeline's whole purpose — do not add a shortcut
around it for convenience.

## 16. No temporary security bypasses

No `if DEBUG: bypass_authorization()`-style code, and no bare
`# TODO: fix security later` comments left in place indefinitely. If a
gap is genuinely temporary, it must be tracked in this repository's
roadmap (docs/roadmap/ROADMAP.md) with what closes it, not left as a
silent comment.

## 17. Reviewability

Every architectural change should be able to answer: what changed, why,
what invariant it affects, what tests prove it, and what security
boundary (if any) it crosses. This document plus
docs/roadmap/ROADMAP.md's commit history already provides this trail —
keep writing real, descriptive commit messages.

## Not yet enforced (tooling gaps — see docs/roadmap/ROADMAP.md)

The following are real goals but are NOT currently automated. Do not
claim they are enforced until they are actually wired in and verified
passing:

- Static linting (planned: `ruff`)
- Static type checking (planned: `mypy`)
- Secret scanning
- Dependency vulnerability scanning
- Pre-commit hooks / CI pipeline
- Code complexity/cyclomatic-complexity limits as an automated check

Until these are wired in and confirmed passing on a real run, they
remain principles this project follows by discipline and code review,
not by automated gate.