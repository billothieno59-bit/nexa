# NEXA Africa Operating System

A modular, constitutionally-governed AI operating system architecture, built
African-first with accessibility, multilingual support (including Sheng), and
safety as foundational design constraints rather than afterthoughts.

## Status

Foundational build — phase 1. The execution, semantic, trust, identity, and
interaction layers are implemented and tested. Perception and knowledge
layers are not yet built.

## Architecture

NEXA is organized into nine canonical "Universal Layers," each with exactly
one authoritative location in the codebase:

| Layer | Responsibility | Location |
|---|---|---|
| USL | Semantic representation | `core/semantic/` |
| UCL | Communication (language, dialects, Sheng) | `core/interaction/communication/` |
| UAL | Accessibility | `core/interaction/accessibility/` |
| UPL | Perception | `core/perception/` |
| UKL | Knowledge | `core/knowledge/` |
| UIL | Identity | `core/identity/` |
| UOL | Orchestration | `core/execution/orchestrator/` |
| UML | Machine/adapter interfaces | `core/execution/uml/` |
| UTL | Trust | `core/governance/trust/` |

Cognition (`core/cognition/`) and the JARVIS interface
(`core/interface/jarvis/`) sit alongside these as core subsystems.

Full architectural rules live in `CONSTITUTION.md` and
`docs/architecture/canonical_module_map.md`. Read both before adding a new
module — duplicate subsystem roots are explicitly prohibited.

## Execution safety model

Every request flows through a fixed, governed pipeline: