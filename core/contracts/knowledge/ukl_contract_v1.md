# NEXA Universal Knowledge Layer (UKL) Contract v1

## Status

Draft — foundational scope only. This contract precedes implementation,
per CONSTITUTION.md Principle 4.

## Purpose

UKL stores durable, reusable facts — knowledge that is true independent
of any one conversation or session. This is explicitly distinct from
`core/cognition/memory/`, which holds session/conversation state (what
was said in this session, when). A fact in UKL should still be true
after the session that produced it has ended.

## Canonical location

`core/knowledge/`

## Boundary with core/cognition/memory/

- Cognition memory: "the user said X in session Y at time Z."
- Knowledge (UKL): "X is true" — a durable fact, independent of which
  session or conversation produced it.

A skill or handler that learns a durable fact during a session may write
it to UKL, but UKL itself does not know or care about sessions.

## Responsibilities

- `Fact` represents a single piece of durable knowledge: subject,
  predicate/relation, value, and provenance (where it came from).
- `FactStore` stores and retrieves facts. Backed by the same SQLite
  pattern already used in `core/cognition/memory/adapters/`, for
  consistency, but a separate database file — knowledge is not session
  memory and must not share storage with it.

## What this must NOT do

- Must not store session/conversation-specific state — that belongs in
  `core/cognition/memory/`.
- Must not infer facts on its own. A Fact is only written when something
  explicitly asserts it; UKL does not perform reasoning or inference in
  this version.

## Core data contract

`Fact`:
- `subject: str`
- `predicate: str`
- `value: str`
- `provenance: str` — where this fact came from (e.g. "user_stated",
  "skill:accessibility.simplify_text")

## Versioning

Adding inference, ontology relationships, or evidence/validation
(beyond simple provenance) requires a new contract version.