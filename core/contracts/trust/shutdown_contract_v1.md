# NEXA Emergency Shutdown Contract v1

## Status

Draft — foundational scope only. This contract precedes implementation,
per CONSTITUTION.md Principle 4.

## Purpose

Defines a single protected capability, `system.shutdown`, that halts the
NEXA process. Authorization is based on possession of a real secret key,
compared in constant time. This contract does NOT define or permit
biometric (voice/face/image) authentication, because no real recognition
model is integrated. A future contract version may add that once a real
model is chosen — it must never be simulated with a hash comparison
disguised as biometric recognition.

## Canonical location

`core/governance/trust/shutdown/`

## Responsibilities

- `EmergencyKeyGuard` verifies a provided key against a configured secret
  (read from the `NEXA_EMERGENCY_KEY` environment variable, never
  hardcoded) using a constant-time comparison.
- If no key is configured, verification fails closed (denies), rather
  than falling back to a default.
- `ShutdownController` authorizes a shutdown request via the key guard
  and, only if authorized, invokes a supplied shutdown callback. The
  controller never performs the actual process exit itself — that is
  the caller's responsibility, so this module stays testable without
  ever terminating a real process during tests.

## What this must NOT do

- Must not claim or imply biometric identity verification unless a real
  recognition model is wired in. `DigestIdentityVerifier`-style
  hash-comparison "identity evidence" is explicitly rejected as
  misleading naming.
- Must not hardcode a default emergency key anywhere in source code.
- Must not log the actual key value, only whether verification
  succeeded or failed.

## Versioning

Adding a real biometric authentication path requires a new contract
version and an explicit decision about which real model/library to
depend on.