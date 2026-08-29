# NEXA Roadmap

This roadmap tracks the target structure from "NEXA Final Canonical
Structure," corrected against CONSTITUTION.md where they disagree, and
organized by what is actually built versus what is planned.

## Naming corrections (read this first)

`core/cognitive/` is wrong; the permanent name is `core/cognition/`.
"UPL" means Universal Perception Layer (`core/perception/`) — never
reused for permissions. If any AI tool proposes `core/cognitive/`, a
redefined UPL, or a top-level `core/memory/`, `core/trust/`,
`core/pipeline/`, `core/agents/`, `core/bus/`, `core/runtime/`,
`core/skills/`, or `core/system/` — stop and check this file and
canonical_module_map.md first.

## Phase 1 — Foundation (DONE)

All nine Universal Layers have real, tested code. Full governed
execution pipeline (Decision -> Planner -> Orchestrator -> Dispatcher ->
Authorization -> Executor), skills economy with enforced authorization
(SkillRegistry -> SkillAuthorizationGate -> trust_bridge -> TrustSession
-> execution_bridge), logging, config validation, emergency shutdown
with real cryptographic key verification.

## Phase 2 — Complete builtin skills catalog (DONE)

The full skills/builtin/ catalog from the canonical structure doc is
now built: accessibility (2 skills), perception (1), knowledge (2),
agriculture, construction, electrical, solar, water_systems, livestock,
education, workforce, entrepreneurship (12 builtin skills total). Plus
4 privileged skills: system.shutdown_nexa, ai.reason, generation.image,
generation.voice.

All safety-relevant skills (agriculture, construction, electrical,
solar, water_systems, livestock) use static, human-curated reference
data with explicit professional-consultation disclaimers — never
fabricated technical instructions, since bad guidance in these domains
can cause real harm.

## Phase 3 — NEXA's own AI (IN PROGRESS)

Three provider abstractions now exist so vendor dependencies can be
replaced without rewriting any skill:
- core/cognition/providers/ — ReasoningProvider (AnthropicReasoningProvider
  real; NexaLocalProvider is a real, working, honest starting point —
  fully offline, matches prompts against real stored facts, narrow scope),
  TranscriptionProvider (OpenAITranscriptionProvider real via Whisper;
  NexaLocalTranscriptionProvider reserved, not_implemented), and
  VisionUnderstandingProvider (AnthropicVisionProvider real;
  NexaLocalVisionProvider reserved, not_implemented)
- core/generation/providers/ — ImageGenerationProvider (OpenAIImageProvider
  real; NexaLocalImageProvider reserved, returns not_implemented) and
  VoiceGenerationProvider (ElevenLabsVoiceProvider real;
  NexaLocalVoiceProvider reserved, returns not_implemented)

Next steps when funded: replace the "not_implemented" local providers
with real trained models. See docs/roadmap/FUNDING_TIER.md for what
that requires (compute, data, team) — nothing here is fabricated as
already working.

## Phase 4 — Remaining architectural gaps

- ~~Wire skills/registry/execution_bridge.py's invoke_skill() into the
  main governed pipeline~~ — CONFIRMED sufficient. Traced
  bootstrap.py -> execution_handler_adapter.py -> execution_bridge.py:
  every registered skill is wrapped as a SkillActionHandler in the
  canonical HandlerRegistry, and SkillActionHandler.handle() calls
  invoke_skill() underneath, so trust resolution and
  SkillAuthorizationGate are never bypassed. No code change was needed.
- ~~core/knowledge/ relationships/querying~~ — DONE. FactStore gained
  get_facts_by_predicate(), get_facts_with_value(), and get_related()
  (cycle-safe breadth-first walk), on top of the existing
  get_facts_about() / get_fact(). No new table or graph engine —
  relationships fall out of the existing subject-predicate-value schema.
- ~~More perception modalities (audio, image, sensor)~~ — DONE.
  AudioPerceptionCapturer, ImagePerceptionCapturer, and
  SensorPerceptionCapturer added, all implementing the existing
  PerceptionCapturer interface, all registered in the default
  PerceptionRegistry.
- ~~Audio/image interpretation providers (speech-to-text, vision
  understanding)~~ — DONE. TranscriptionProvider (OpenAITranscriptionProvider
  real via Whisper; NexaLocalTranscriptionProvider reserved,
  not_implemented) and VisionUnderstandingProvider
  (AnthropicVisionProvider real; NexaLocalVisionProvider reserved,
  not_implemented) added to core/cognition/providers/, each with its
  own router (transcription_router.py, vision_router.py).
- ~~ResourceTransactionHandler~~ — DONE, with an explicitly documented
  assumption (no formal product spec existed): a "resource
  transaction" is treated as a signed delta against a named,
  per-subject running balance, stored via the existing FactStore
  (predicate "resource_balance:<resource_name>"). Fails closed on
  malformed input and on any transaction that would take a balance
  below zero.
- ~~Voice commands~~ — DONE. core/semantic/parser/voice_command_bridge.py
  resolves a transcribed audio PerceptionEvent through the same
  global_usl_mapper text commands use. See
  docs/roadmap/FUTURE_multimodal_identity.md for what's still open:
  face/image recognition and speaker verification remain unbuilt, and
  wiring resolved voice/text intents into actual governed execution is
  an unresolved architecture choice among three existing, unconnected
  dispatch mechanisms (core/applications/api/dispatcher.py's
  ExecutionGateway path, core/cognition/routing/router.py's
  SemanticRouter, and the core/execution/ orchestrator/planner chain).
- Multimodal identity recognition (face/image, speaker verification) —
  still planned in docs/roadmap/FUTURE_multimodal_identity.md, pending
  backend decisions.

## Phase 5+ — Not started

core/events/ (message bus), multi-surface applications (desktop/mobile/
web), core/platform/, remaining core/services/ (storage, monitoring,
telemetry), community/enterprise skill tiers, core/spatial/ (3D/AR/VR),
tools/, scripts/ beyond what exists.

## Applications API layer (core/applications/api/)

Real, tested: ApiGatewayEngine (constant-time key auth via hmac,
TokenBucketRateLimiter, delegates to ApiRequestDispatcher),
ApiRequestDispatcher (resolve-only — never executes handlers directly,
delegates to the canonical ExecutionGateway). Note: this dispatcher
resolves action+params payloads; it does not yet consume a USL
resolved_intent_token from either text or voice input (see Phase 4
voice commands entry above).

## Frontend (web/, root-level static HTML/CSS/JS)

No build tooling — plain index.html/style.css/script.js, opens
directly in any browser. React/Vite/Tailwind setup (src/, package.json,
node_modules/) was removed; this static version is the sole frontend.
web/api/dashboard.py now delegates to core/interface/api/dashboard.py
(previously duplicated the logic with a bug — calling a nonexistent
SkillRegistry.manifests() method and a hardcoded stale test count).

Done: tropical color palette applied (Deep Ocean/Palm Emerald/Tropical
Mint/Sunset Gold/Walnut/Ivory), glass-sphere login orb with internal
swirl, tropical-leaf accents on the login screen, subtle (4% opacity)
geometric card pattern, dashboard wired to real backend state (skill
counts, provider connection status) via core/interface/api/dashboard.py.

Not yet done: typography still Space Grotesk/Inter/JetBrains Mono (no
font change has been made); header/login screen still reads "Admin"
(no name change has been made); web/components/jarvis_orb.js exists
but its integration with the dashboard data hasn't been traced/verified
here yet.

## Known production-readiness gaps

- ~~No structured logging~~ — DONE
- ~~SQLiteMemoryAdapter defaults to `:memory:`~~ — DONE
- ~~SemanticRouter.dispatch() does not catch handler exceptions~~ — DONE
- ~~Gateway/Executor registry singleton bug~~ — DONE
- ~~Identity/authorization coupling~~ — DONE (TrustSession)
- ~~No config validation at startup~~ — DONE
- ~~ResourceTransactionHandler is still a no-op~~ — DONE, see Phase 4.
- SkillAuthorizationGate's granted_permissions now correctly derives
  from a real TrustSession via trust_bridge.py — DONE.