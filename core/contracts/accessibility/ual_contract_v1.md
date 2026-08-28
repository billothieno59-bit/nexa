# NEXA Universal Accessibility Layer (UAL) Contract v1

## Status

Draft — foundational scope only. This contract precedes implementation,
per CONSTITUTION.md Principle 4.

## Purpose

UAL is responsible for representing a person's accessibility needs and
preferences as structured data, and for adapting NEXA's output to those
needs. UAL does not implement assistive hardware or third-party
technology itself (e.g. it does not implement a screen reader or a
text-to-speech engine) — it defines what a person needs and provides
adapters that reshape output to meet that need, some of which may
delegate to real external assistive technology later.

## Canonical location

`core/interaction/accessibility/`

## Responsibilities

- Represent an `AccessibilityProfile`: a structured, honest description
  of a person's stated accessibility needs and preferences.
- Provide output adapters that transform NEXA's responses to match a
  profile (e.g. simplifying sentence structure, expanding abbreviations)
  — implemented only where the transformation can honestly be performed
  without external technology NEXA does not yet integrate with.
- Fail closed / pass through unmodified when a requested accommodation
  cannot yet be honestly performed, rather than pretending to have
  performed it.

## What UAL must NOT do

- Must not claim to support an accommodation it cannot actually perform
  (e.g. must not claim "sign language output" unless a real sign
  language rendering system is wired in — that is a Phase 6 spatial/
  generation concern, not something to fabricate here now).
- Must not infer a disability or accessibility need the person has not
  stated. Profiles are built from explicit, stated preferences only.
- Must not duplicate UCL's (communication layer) responsibility for
  language, dialect, or translation. Simplifying English sentence
  structure for cognitive accessibility is a UAL concern; translating
  between languages is UCL's.

## Core data contract

`AccessibilityProfile`:

- `profile_id: str`
- `needs_simplified_language: bool`
- `needs_screen_reader_friendly_output: bool`
- `preferred_reading_level: Optional[str]` (e.g. "simple", "standard")
- `metadata: dict` — for future, explicitly-stated preferences not yet
  covered by a named field

## Versioning

Adding a new accommodation type or changing the profile shape requires a
new contract version, per CONSTITUTION.md.