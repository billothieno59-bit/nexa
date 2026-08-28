# Future Work: Multimodal Identity Recognition + Voice Commands

Status: PLANNED, NOT STARTED. No code exists for this yet. This document
exists so the shape is saved before implementation begins, per
CONSTITUTION.md Principle 4 (contracts before implementation).

## Goal

NEXA recognizes the founder through voice, video, and image, and accepts
spoken commands, while keeping "recognition" and "authorization" as
separate concerns — recognition produces evidence; authorization is a
capability decision, same pattern already used by
`core/governance/trust/shutdown/`.

## Decisions still pending (must be made before any code is written)

1. **Face/image recognition backend** — local (`face_recognition`/dlib,
   or OpenCV DNN) vs. cloud API (Azure Face, AWS Rekognition). Local
   keeps biometric data off third-party servers; cloud is easier to
   install on Windows but sends face data externally.
2. **Voice** — speaker verification (who is speaking) vs. voice commands
   (what is said) vs. both. Speaker verification is a harder local
   problem (`Resemblyzer`/`SpeechBrain` vs. a cloud API). Voice commands
   only need speech-to-text (e.g. local Whisper or `speech_recognition`).
3. **Enrollment storage** — where reference face/voice samples are kept
   and how they're encrypted at rest. Leaning local-only, encrypted, but
   not finalized.

## Planned structure (paths only — do not create empty files for these
## until the decisions above are made; an empty stub here would invite
## the same fabricated-biometrics risk already rejected once this session)