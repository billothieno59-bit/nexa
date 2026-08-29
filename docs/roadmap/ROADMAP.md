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
with real cryptographic key verification. execution_bridge.invoke_skill()
also enforces a per-caller TokenBucketRateLimiter before authorization —
this existed as a standalone class but was never wired to anything until
its NameError bug (missing bucket lookup in allow_request()) was fixed
and it was connected as the single enforcement point for all skill calls.

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

knowledge.recall_fact also exposes FactStore.get_related() (cycle-safe
breadth-first relationship walk) via an optional max_depth parameter,
so relationship queries go through the same governed, authorized path
as flat fact lookups.

## Phase 3 — NEXA's own AI (IN PROGRESS)

Three provider abstractions now exist so vendor dependencies can be
replaced without rewriting any skill:
- core/cognition/providers/ — ReasoningProvider (AnthropicReasoningProvider
  real; NexaLocalProvider is a real, working, honest starting point —
  fully offline, matches prompts against real stored facts, narrow scope)
- core/generation/providers/ — ImageGenerationProvider (OpenAIImageProvider
  real; NexaLocalImageProvider reserved, returns not_implemented) and
  VoiceGenerationProvider (ElevenLabsVoiceProvider real;
  NexaLocalVoiceProvider reserved, returns not_implemented)
- core/cognition/providers/ — TranscriptionProvider
  (OpenAITranscriptionProvider real via Whisper; NexaLocalTranscriptionProvider
  reserved) and VisionUnderstandingProvider (AnthropicVisionProvider real;
  NexaLocalVisionProvider reserved)

generation.voice (VOICE.GENERATE, founder-only) is proven working through
the FULL real governed pipeline end to end — rate limit -> trust session
resolution -> CONSTITUTIONAL_FOUNDER role match -> authorization ->
ElevenLabsVoiceProvider — not just tested in isolation via
SkillAuthorizationGate. See skills/privileged/tests/test_voice_generation_integration.py.
Only the outbound network call is faked in tests.

Next steps when funded: replace the "not_implemented" local providers
with real trained models. See docs/roadmap/FUNDING_TIER.md for what
that requires (compute, data, team) — nothing here is fabricated as
already working.

## Phase 4 — Remaining architectural gaps

- ~~Wire skills/registry/execution_bridge.py's invoke_skill() into the
  main governed pipeline~~ — CONFIRMED sufficient. Every registered
  skill is wrapped as a SkillActionHandler in the canonical
  HandlerRegistry, and SkillActionHandler.handle() calls invoke_skill()
  underneath, so trust resolution and SkillAuthorizationGate are never
  bypassed.
- ~~core/knowledge/ relationships/querying~~ — DONE, and exposed through
  the governed knowledge.recall_fact skill (see Phase 2).
- ~~More perception modalities (audio, image, sensor)~~ — DONE.
  AudioPerceptionCapturer, ImagePerceptionCapturer, and
  SensorPerceptionCapturer implement the existing PerceptionCapturer
  interface, all registered in the default PerceptionRegistry.
- ~~Audio/image interpretation providers~~ — DONE (see Phase 3).
- ~~Voice commands~~ — DONE. core/semantic/parser/voice_command_bridge.py
  transcribes an audio PerceptionEvent via the configured
  TranscriptionProvider, then resolves the transcribed text through
  the SAME global_usl_mapper text commands already use — no separate
  voice-only intent table. Fails closed (governed_execution_authorized
  stays False) on any transcription problem, so a spoken command never
  gets guessed at from a partial or failed transcription.
- ~~ResourceTransactionHandler~~ — DONE, with an explicitly documented
  assumption (no formal product spec existed): a "resource
  transaction" is treated as a signed delta against a named,
  per-subject running balance, stored via the existing FactStore
  (predicate "resource_balance:<resource_name>"). Fails closed on
  malformed input and on any transaction that would take a balance
  below zero. Still pending product confirmation that this matches
  the intended meaning.
- ~~Live execution pipeline state~~ — DONE. core/execution/state/pipeline_state.py's
  PIPELINE_STATE existed but was never called by anything. Now
  ExecutionPipeline.process() (core/execution/pipeline/pipeline.py)
  advances it at each real stage transition (Planner/Orchestrator/
  Dispatcher/Authorization/Executor), and a short-circuited request
  (blocked/awaiting_confirmation) correctly leaves state at the last
  stage that actually ran rather than claiming it reached further.
- Multimodal identity recognition (voiceprint/passphrase confirmation)
  — NOT started. Requires a product decision that hasn't been made:
  how should NEXA confirm who's speaking — a known voice sample, a
  spoken passphrase, or something else. Voice COMMANDS (what to do)
  are done and separate from voice