# NEXA Change Log

Every change made to this project, in order, so any builder can see
what exists and why without reconstructing it from git log. Newest
entry at the top. Each entry lists exactly what changed and in which
files, verified against the actual file contents at time of writing.

---

## 2026-08-29 — resource.check_balance skill; http_server.py line-length fix; unreviewed code noted

**What changed:** Three things in this pass:

1. Added `skills/builtin/resource_check_balance.py` — a read-only
   builtin skill (`resource.check_balance`, permission
   `RESOURCE.READ`) that reads a resource balance back from
   `FactStore`, the same way `knowledge.recall_fact` completes the
   read side of `knowledge.remember_fact`. Read-only counterpart to
   `ResourceTransactionHandler` (`core/execution/executor/action_handlers.py`),
   which could previously only write balances, never read them back
   through a governed, authorized path. Registered in
   `skills/registry/bootstrap.py` alongside the other builtin skills.
   Note: `RESOURCE_PREDICATE_PREFIX` is intentionally duplicated in
   this file rather than imported from `action_handlers.py`, to avoid
   a circular import (`action_handlers.py` imports
   `skills.registry.bootstrap`, which registers this skill module) —
   must be kept identical to `action_handlers.py`'s copy.

2. Fixed a `ruff` line-length violation in
   `core/applications/api/http_server.py:70` — a nested nine-way
   ternary computing an HTTP status code from a skill result status.
   Extracted into a small `_http_status_for()` helper function;
   behavior is identical, just readable and within the 120-char limit.

3. **Substantial code arrived in the same commit that was not built or
   reviewed here**, swept in by `git add -A`:
   `core/applications/api/web_skill_gateway.py`,
   `core/applications/api/http_server.py` (the file this pass edited,
   but its original content/design predates this pass),
   `core/applications/cli.py`, `core/execution/pipeline/`,
   `core/execution/state/`, `core/governance/trust/tests/test_voice_identity.py`,
   and a restructured `web/` (now `web/index.html`, `web/script.js`,
   `web/styles/style.css`). None of this has been read or verified
   here beyond confirming it doesn't break `ruff`/`pytest` — it should
   not be assumed to follow the same conventions or assumptions
   documented elsewhere in this log until actually reviewed.

**Files touched:**
- `skills/builtin/resource_check_balance.py` (new)
- `skills/builtin/tests/test_resource_check_balance.py` (new)
- `skills/registry/bootstrap.py` (modified — one import, one
  registration line added)
- `core/applications/api/http_server.py` (modified — line-length fix)

**Verified:** `ruff check . --fix` — all checks passed, 0 remaining
errors. `python -m pytest` — 432 passed, 0 failed, 4.40s.

---

## 2026-08-29 — Removed dead duplicate jarvis_orb.js; docs synced with code

**What changed:** Two unrelated cleanups made in the same pass:

1. Deleted `web/components/jarvis_orb.js` — a standalone `attachJarvisOrb()`
   module never imported by `index.html` or `script.js` (confirmed
   zero references anywhere in the repo). It duplicated the orb-state
   logic already implemented directly in `script.js`, but with the
   pre-retheme color palette (`#00C2FF` cyan, `#8B5CF6` violet,
   `#FFB703` gold) — inconsistent with the tropical palette already
   applied everywhere else. Dead, duplicate, and stale; removed rather
   than left to confuse a future reader.

2. `docs/roadmap/ROADMAP.md` and `docs/roadmap/FUTURE_multimodal_identity.md`
   updated to reflect that `core/semantic/parser/voice_command_bridge.py`
   (voice commands) is real and tested — both docs previously said this
   was "pending backend decisions" / "PLANNED, NOT STARTED," which was
   no longer true. Also documented a concrete, traced finding: the
   canonical `Decision -> ExecutionPlanner -> ExecutionOrchestrator ->
   ExecutionExecutor` pipeline's `create_plan()` currently hardcodes
   `PlanStep.action` to the literal strings `"respond"` or
   `"await_confirmation"` — never to the actual intent token. This
   means no registered handler (not `ResourceTransactionHandler`, not
   any skill) can currently fire through this pipeline for text OR
   voice input. This is a pre-existing gap in core planning logic, not
   specific to voice, and changing `create_plan()`'s mapping is a
   meaningful behavior change to an already-tested module — flagged
   for a decision rather than changed silently.

**Files touched:**
- `web/components/jarvis_orb.js` (deleted)
- `docs/roadmap/ROADMAP.md` (modified)
- `docs/roadmap/FUTURE_multimodal_identity.md` (modified)

**Verified:** manual `grep` across the full repo confirmed zero
remaining references to `jarvis_orb.js` or `attachJarvisOrb` before
deletion. Full `ruff check . --fix` / `python -m pytest` not yet
re-run against this specific change — pending.

**Open decision, not yet made:** how a resolved intent token
(from either `voice_command_bridge.py` or a future text equivalent)
should actually reach a registered handler, given the `create_plan()`
gap above. Needs a decision before any wiring code is written.

---

## 2026-08-29 — Voice generation integration test fix (CONFIRMED)

**What changed:** `skills/privileged/tests/test_voice_generation_integration.py`
had a monkeypatch scoping bug: it patched
`core.generation.providers.voice_router.get_voice_provider` (where the
function is defined), but `skills/privileged/voice_generation.py`
imports it via `from ... import get_voice_provider` (line 18), which
binds a separate reference into `voice_generation.py`'s own namespace.
Patching the origin never touched the copy the skill actually calls,
so the real `ElevenLabsVoiceProvider` ran unpatched, found no API key,
and returned `"not_configured"` instead of the test's faked `"ok"`.
Fixed by changing the patch target to
`skills.privileged.voice_generation.get_voice_provider` — the one line
the test needed, no production code changed.

**Files touched:**
- `skills/privileged/tests/test_voice_generation_integration.py` (modified, 1 line)

**Verified:** `python -m pytest skills\privileged\tests\test_voice_generation_integration.py -v`
— 4 passed (up from 1 failed / 3 passed). Full suite:
`python -m pytest` — 385 passed, 0 failed, 3.56s.

**Note:** this test file, `voice_generation.py`'s current form,
`core/interface/api/`, `web/`, `core/semantic/parser/`, and the rate
limiter did not originate in this conversation — first seen when
reading the repo to diagnose this failure.

---

## 2026-08-28 — Perception interpretation providers + ResourceTransactionHandler (CONFIRMED)

**What changed:** Added `TranscriptionProvider` and
`VisionUnderstandingProvider` interfaces to
`core/co