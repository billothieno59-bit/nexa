# NEXA African Operating System
# Canonical Architecture v1.0

Status: Foundational Build
Authority: CONSTITUTION.md

## 1. Purpose

This document defines the canonical architectural organization of NEXA African Operating System.

The constitution remains the highest-level authority. This document translates constitutional principles into concrete subsystem boundaries and canonical locations.

## 2. Canonical Universal Layers

| Universal | Canonical Path |
|---|---|
| UCL | core/interaction/communication/ |
| UAL | core/interaction/accessibility/ |
| UPL | core/perception/ |
| USL | core/semantic/ |
| UKL | core/knowledge/ |
| UIL | core/identity/ |
| UOL | core/execution/orchestrator/ |
| UML | core/execution/uml/ |
| UTL | core/governance/trust/ |

## 3. Cognition

Canonical path:

core/cognition/

Responsibility:

- reasoning
- planning
- memory
- learning
- decision processes

Cognition must remain independent of human language and presentation interfaces.

## 4. JARVIS

Canonical path:

core/interface/jarvis/

JARVIS is the canonical NEXA human-facing interface runtime.

JARVIS may provide:

- conversational interaction
- voice interaction
- text interaction
- visual interaction
- response presentation
- assistant identity presentation
- accessibility integration

JARVIS must not own:

- semantic reasoning
- knowledge
- cognition
- orchestration
- execution
- trust authority

The user-facing assistant name is configurable.

"JARVIS" identifies the canonical interface subsystem, not a mandatory user-facing name.

## 5. Communication

Canonical path:

core/interaction/communication/

UCL is responsible for communication representations between humans, systems, and NEXA.

UCL may support:

- natural languages
- dialects
- Sheng
- code-switching
- language identification
- communication normalization
- translation
- response-language selection

Communication representations must not become the internal foundation of cognition.

## 6. Semantic Foundation

Canonical path:

core/semantic/

USL provides language-independent semantic representation.

Human language enters NEXA through communication and is transformed into semantic meaning before core reasoning.

Semantic meaning must remain independent from the presentation language.

## 7. Architecture Rule

Every subsystem must have:

1. one canonical location
2. one defined responsibility
3. one authoritative contract
4. replaceable implementations

Duplicate architectural roots are prohibited.

## 8. Implementation Rule

Architecture and contracts precede implementation.

No major subsystem should be implemented until its responsibility and contract have been defined and reviewed.
