# NEXA Funding-Dependent Roadmap

This separates what NEXA can build with continued engineering time alone
from what genuinely requires real capital (compute, data, a team). This
distinction matters for planning and for anyone evaluating the project —
neither tier should be misrepresented as the other.

## Achievable now, engineering time + pay-per-use API cost only

No upfront capital required — same pattern as ai.reason,
generation.image, and generation.voice: an injectable API client, fails
closed without a configured key, ordinary per-request usage cost instead
of infrastructure investment. NEXA does NOT own the underlying model in
this tier — it depends on Anthropic, OpenAI, and ElevenLabs respectively:

- More builtin skills: translation, construction, electrical, solar,
  water systems, livestock, education, workforce, entrepreneurship —
  the full skills/builtin/ catalog from the canonical structure doc
- More perception modalities using free/low-cost libraries or APIs
- More accessibility accommodations
- core/knowledge/ expansion (querying, simple relationships)
- Continued hardening: more tests, more contracts, more of
  ENGINEERING_RULES.md's "not yet enforced" tooling wired in
- Image generation (generation.image, via OpenAI) — DONE, dependent on OpenAI
- Voice/audio generation (generation.voice, via ElevenLabs) — DONE, dependent on ElevenLabs
- AI reasoning (ai.reason, via Anthropic) — DONE, dependent on Anthropic
- Video generation via a real third-party API — same pattern, not yet built

## Requires real upfront capital (compute + data + team) — the path to NEXA owning its own models, independent of any other AI company

This is the explicit future goal when funding exists: replace the
API-dependent skills above with models NEXA trains, hosts, and runs
itself, so NEXA stops depending on Anthropic, OpenAI, or ElevenLabs:

- A genuinely competent LOCAL LLM, trained from scratch, replacing
  ai.reason's dependency on Anthropic — training data at scale, real
  GPU/TPU compute, realistically $ hundreds of thousands to millions
- NEXA's own local image generation model, replacing generation.image's
  dependency on OpenAI — real training data (licensed or curated
  images) and real compute to train a diffusion model
- NEXA's own local voice generation model, replacing generation.voice's
  dependency on ElevenLabs — real voice training data and compute
- Real multimodal biometric identity (voice/face recognition) trained
  or hosted as NEXA's own model — see
  docs/roadmap/FUTURE_multimodal_identity.md
- core/spatial/ (3D engine, AR/VR, holographic visualization) — needs
  dedicated graphics/XR engineering, not achievable as an incremental
  skill addition
- Any meaningful scaling of core/platform/, core/services/ (monitoring,
  telemetry at real production scale) beyond what a single developer
  needs for local development

Each API-dependent skill above is written with an injectable client
specifically so that swapping the API-backed implementation for a
locally-trained model later is a contained change — the skill's
permission gate, manifest, and fail-closed behavior stay the same; only
what's behind `_get_client()` changes.

## Not achievable regardless of funding

- True general intelligence / AGI. This is an open research problem;
  no amount of money changes that. NEXA is, and will remain, a narrow
  AI system, same as nearly every deployed AI system in the world today.