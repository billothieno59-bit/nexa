# NEXA Change Log

Every change made to this project, in order, so any builder can see
what exists and why without reconstructing it from git log. Newest
entry at the top. Each entry lists exactly what changed and in which
files, verified against the actual file contents at time of writing.

---

## 2026-09-02 — Confirmed: NEXA runs live in a browser, full pipeline fires end-to-end

**What changed:** No code changed in this pass — this entry records a
live, verified confirmation that the existing `core/applications/api/http_server.py`
Flask server actually works end-to-end, browser to governed pipeline
and back.

**Verified, live, on real requests:**
1. `python -m core.applications.api.http_server` starts cleanly,
   registers all 18 skills (14 builtin, 4 privileged), serves on
   `http://127.0.0.1:5000`.
2. `POST /api/skills/agriculture.crop_advisor` with
   `{"crop": "maize"}` → executed successfully, real guidance +
   disclaimer returned.
3. `POST /api/skills/finance.literacy_advisor` with
   `{"topic": "savings"}` → executed successfully, same real path.
4. `POST /api/skills/system.shutdown_nexa` (a privileged skill) →
   correctly **denied** with `"Only builtin skills are reachable from
   the web client."` — confirms the privileged-skill web lockout
   documented in `http_server.py`'s docstring is real, not just
   claimed.

Full chain confirmed live: HTTP request -> Flask route ->
`web_skill_gateway.run_web_skill()` -> rate limiting -> trust session
resolution -> `SkillAuthorizationGate` -> the actual skill handler ->
JSON response.

**Noted for later, not acted on:** the web client is explicitly a
"fixed web client identity" that never has `CONSTITUTIONAL_FOUNDER`
(per `http_server.py`'s own docstring) — meaning renaming the login
screen's "Admin" to "Bill" (proposed earlier, never done) would now be
actively misleading in this context, since a web visitor is never
actually authenticated as the founder. Any future identity/login work
on the web frontend needs to account for this rather than just
swapping display text.

**Files touched:** none.

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

2. Fixed a `ruff` line-length violation in
   `core/applications/api/http_server.py:70` — a nested nine-way
   ternary computing an HTTP status code from a skill result status.
   Extracted into a small `_http_status_for()` helper function.

3. Substantial code arrived in the same commit that was not built or
   reviewed here, swept in by `git add -A`:
   `core/applications/api/web_skill_gateway.py`,
   `core/applications/cli.py`, `core/execution/pipeline/`,
   `core/execution/state/`, `core/governance/trust/tests/test_voice_identity.py`,
   and a restructured `web/` folder. Later confirmed (2026-09-02
   entry above) that `web_skill_gateway.py` and `http_server.py`
   genuinely work end-to-end.

**Files touched:**
- `skills/builtin/resource_check_balance.py` (new)
- `skills/builtin/tests/test_resource_check_balance.py` (new)
- `skills/registry/bootstrap.py` (modified)
- `core/applications/api/http_server.py` (modified — line-length fix)

**Verified:** `ruff check . --fix` — all checks passed. `python -m pytest`
— 432 passed, 0 failed.

---

## 2026-08-29 — finance.literacy_advisor and housing.tenancy_rights_advisor added

**What changed:** Two new builtin skills, matching the existing
curated-reference-data + disclaimer pattern used by
`agriculture.crop_advisor` and the other safety-relevant advisors:

- `finance.literacy_advisor` (`skills/builtin/financial_literacy_advisor.py`)
  — general financial literacy reference (savings, mobile money
  safety, budgeting, credit/loans basics). Explicitly not financial
  advice or a product recommendation.
- `housing.tenancy_rights_advisor` (`skills/builtin/tenancy_rights_advisor.py`)
  — general tenant/landlord reference (deposits, notice periods, rent
  increases, repairs). Explicitly not legal advice.

Both use static, human-curated reference tables, not generated
content, consistent with `CONSTITUTION.md`'s requirement for any
domain where incorrect guidance can cause real harm.

**Files touched:**
- `skills/builtin/financial_literacy_advisor.py` (new)
- `skills/builtin/tests/test_financial_literacy_advisor.py` (new)
- `skills/builtin/tenancy_rights_advisor.py` (new)
- `skills/builtin/tests/test_tenancy_rights_advisor.py` (new)
- `skills/registry/bootstrap.py` (modified)

**Verified:** `ruff check . --fix` — all checks passed (after fixing
3 line-length errors in `tenancy_rights_advisor.py`'s `"notes"`
strings in a follow-up pass). `python -m pytest` — 444 passed, 0
failed.

---

## 2026-08-29 — Removed superseded prototype frontend (web/index.html, web/script.js, web/styles/)

**What changed:** Deleted `web/index.html`, `web/script.js`, and
`web/styles/style.css` — confirmed to be an earlier, cruder prototype
of the dashboard, not in-progress or newer work. Evidence: hardcoded
pre-retheme colors (`#00E5A8`, `#00C2FF`, `#8B5CF6`, `#FFB703`), no
login screen, no leaf accents, no glass-sphere orb, skills list
hardcoded as static `<span>` tags rather than fetched from
`/api/skills`, clock/orb driven by pure local JS with no backend
calls at all. Confirmed via `grep` that nothing in the codebase
referenced these files before deletion.

**Files touched:**
- `web/index.html` (deleted)
- `web/script.js` (deleted)
- `web/styles/style.css` (deleted)

**Verified:** `ruff check . --fix` — all checks passed. `python -m pytest`
— 444 passed, 0 failed (no tests exercised these files).

---

## 2026-08-29 — Removed dead duplicate jarvis_orb.js; docs synced with code

**What changed:** Two unrelated cleanups made in the same pass:

1. Deleted `web/components/jarvis_orb.js` — a standalone `attachJarvisOrb()`
   module never imported by `index.html` or `script.js` (confirmed
   zero references anywhere in the repo). It duplicated the orb-state
   logic already implemented directly in `script.js`, but with the
   pre-retheme color palette — inconsistent with the tropical palette
   already applied everywhere else.

2. `docs/roadmap/ROADMAP.md` and `docs/roadmap/FUTURE_multimodal_identity.md`
   updated to reflect that `core/semantic/parser/voice_command_bridge.py`
   (voice commands) is real and tested. Also documented a concrete,
   traced finding: the canonical `Decision -> ExecutionPlanner ->
   ExecutionOrchestrator -> ExecutionExecutor` pipeline's
   `create_plan()` currently hardcodes `PlanStep.action` to the
   literal strings `"respond"` or `"await_confirmation"` — never to
   the actual intent token. This means no registered handler