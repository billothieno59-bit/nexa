# NEXA Universal Perception Layer (UPL) Contract v1

## Status

Draft — foundational scope only. This contract precedes implementation,
per CONSTITUTION.md Principle 4.

## Purpose

UPL is responsible for converting raw sensory input (text, audio, image,
video, sensor readings) into structured, validated `PerceptionEvent`
objects. It observes; it does not interpret meaning and does not decide
anything.

## Canonical location

`core/perception/`

## Responsibilities

- Accept raw input from a given modality (text, audio, image, video,
  sensor).
- Validate and structure that input into an immutable `PerceptionEvent`.
- Attach modality, source, and timestamp metadata to every event.
- Provide one capturer implementation per modality behind a common
  interface, so new modalities can be added without changing callers.

## What UPL must NOT do

- Must not interpret linguistic meaning, dialect, or code-switching.
  That is UCL's responsibility (`core/interaction/communication/`).
- Must not extract language-independent semantic meaning. That is USL's
  responsibility (`core/semantic/`).
- Must not decide, plan, or execute anything. That is cognition/execution's
  responsibility.
- Must not persist perception events long-term. That is a memory/knowledge
  concern (`core/cognition/memory/`, future `core/knowledge/`), not
  perception's.

## Boundary with UCL (communication)

Raw audio-to-text transcription (mechanical speech recognition) is a UPL
concern — it produces a `PerceptionEvent` with `modality="speech"` and a
`raw_text` field. What that text *means*, including Sheng/dialect
normalization and code-switching, is UCL's job once the event leaves UPL.
UPL never touches meaning.

## Core data contract

Every capturer returns a `PerceptionEvent`:

- `modality: str` — e.g. "text", "audio", "image", "sensor"
- `source: str` — where the input came from (e.g. "cli", "microphone",
  "camera_1")
- `payload: Any` — the raw or minimally-processed input
- `timestamp: float` — Unix time the event was captured
- `metadata: dict` — modality-specific extra fields (e.g. confidence
  score for a future speech capturer)

## Versioning

Changes to the `PerceptionEvent` shape or capturer interface require a new
contract version (`upl_contract_v2.md`) per CONSTITUTION.md's rule that
architectural evolution happens through explicit versions, never silent
changes.