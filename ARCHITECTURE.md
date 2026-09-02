NEXA Architecture
Overview

NEXA is a modular AI platform designed around governed cognition, perception,
knowledge, identity, communication, orchestration, execution, and trust.

NEXA is built as a layered system so that intelligence, decision-making,
authorization, and execution remain separate and testable.

Core Flow
User
  ↓
Interface
  ↓
Application / API Layer
  ↓
Communication
  ↓
Perception / Knowledge
  ↓
Cognition
  ↓
Decision
  ↓
Planning
  ↓
Orchestration
  ↓
Authorization
  ↓
Execution
  ↓
Skills / Providers / External Systems

No interface component should bypass the governed application and execution
pipeline.

Architectural Layers
USL — Universal Semantic Layer

The semantic layer provides structured representations and contracts for
meaning, intent, entities, actions, and system communication.

USL provides the semantic foundation used by higher-level NEXA components.

UCL — Universal Communication Layer

The communication layer manages communication between NEXA components and
external interfaces.

It provides structured communication without allowing communication paths
to bypass governance.

UAL — Universal Accessibility Layer

The accessibility layer provides mechanisms for interacting with NEXA through
different accessibility and interaction modes.

UPL — Universal Perception Layer

The perception layer handles incoming information such as:

Text
Images
Audio
Sensors
Other supported input sources

Perception converts external input into information that can be processed by
the cognitive system.

UKL — Universal Knowledge Layer

The knowledge layer manages structured knowledge and knowledge-related
operations.

It provides a foundation for storing, retrieving, and working with
knowledge while remaining separate from reasoning and execution.

UIL — Universal Identity Layer

The identity layer manages identity-related system concerns.

Identity is kept separate from authorization so that knowing who or what is
requesting an operation does not automatically grant permission to perform
that operation.

UOL — Universal Orchestration Layer

The orchestration layer coordinates complex operations across NEXA
subsystems.

It is responsible for coordinating approved work rather than bypassing
authorization.

UML — Universal Machine Interface Layer

The machine interface layer provides controlled interfaces between NEXA and
machines, devices, or other external systems.

Machine interaction must remain governed by the authorization and execution
architecture.

UTL — Universal Trust Layer

The trust layer provides governance and safety mechanisms.

NEXA follows a fail-closed approach:

Unknown       → Block
Unauthorized → Block
Invalid       → Block
Unsafe        → Block
Approved      → Continue
Cognition

Cognition is responsible for processing information and supporting
intelligent behavior.

Major cognitive responsibilities include:

Context
Attention
Memory
Personality
Goals
Reasoning
Planning
Decision support
Routing

Cognition does not directly perform privileged external actions.

Decision

The decision layer determines what NEXA intends to do based on available
context, goals, reasoning, policies, and system state.

A decision is not equivalent to execution.

The system must maintain a boundary between:

Decision
   ↓
Planning
   ↓
Execution
Planning

Planning transforms an approved intention into an executable plan.

The planner must produce structured work that can be evaluated by downstream
governance components.

Planning does not grant authorization.

Execution Pipeline

NEXA uses a governed execution pipeline:

Decision
   ↓
Execution Planner
   ↓
Execution Orchestrator
   ↓
Execution Dispatcher
   ↓
Authorization
   ↓
Execution Executor
   ↓
Gateway
   ↓
Handler / Skill
   ↓
External System

Each stage has a distinct responsibility.

Dispatcher

The dispatcher determines whether work is ready for downstream processing.

Authorization

Authorization determines whether the requested operation is permitted.

Executor

The executor performs only work that has successfully passed the required
governance checks.

Blocked or unauthorized operations must never reach execution.

Gateway

The gateway provides a controlled boundary between execution infrastructure
and registered capabilities.

Handler / Skill

Handlers and skills perform the actual capability-specific operation.

Skills

NEXA uses a registry-based skill architecture.

Skills may represent capabilities such as:

Knowledge operations
Accessibility operations
Perception operations
Reasoning
Image generation
Voice generation
Other governed capabilities

Skills must remain subject to the applicable trust, authorization, and
execution rules.

Privileged skills must not be exposed through unrestricted public routes.

Application and API Layer

The application/API layer provides controlled access to NEXA functionality.

The web interface communicates with NEXA through this layer.

The API layer must:

Validate requests
Enforce allowed methods
Validate request formats
Protect privileged capabilities
Prevent unauthorized execution
Avoid exposing secrets
Route requests through governed system components

The interface must never directly execute privileged system operations.

Web Interface

The web interface provides the user-facing entry point to NEXA.

The intended architecture is:

Web UI
  ↓
HTTP API
  ↓
Application Layer
  ↓
NEXA Core
  ↓
Governance
  ↓
Execution

The interface is therefore a client of NEXA rather than an independent
execution system.

Security Principles

NEXA follows these core security principles:

Fail Closed

When the system cannot establish that an operation is safe and authorized,
the operation must not execute.

Separation of Identity and Authorization

Identity establishes who or what is making a request.

Authorization determines what that identity is permitted to do.

No Hidden Execution

Execution must occur through the governed execution architecture.

Privileged Capability Protection

Privileged capabilities must not be accidentally exposed through public
interfaces.

Explicit Governance

Important actions should be traceable through the decision, planning,
authorization, and execution chain.

Safe Unknown Handling

Unknown operations, unknown statuses, malformed requests, and invalid
capabilities should fail safely.

Testing Architecture

Every major subsystem should have automated tests.

The current verified project baseline is:

426 tests passing

The test suite covers major areas including:

Execution
Authorization
Dispatcher
Executor
Gateway
Orchestrator
Planner
Semantic contracts
Skills
API
Dashboard
HTTP server
Web skill gateway

The test suite is part of the architecture and must remain green as the
system evolves.

Development Principle

NEXA should be developed as an integrated system rather than as disconnected
features.

The preferred progression is:

Interface
   ↓
Application / API
   ↓
Brain / Cognition
   ↓
Decision
   ↓
Planning
   ↓
Orchestration
   ↓
Authorization
   ↓
Execution
   ↓
Skills
   ↓
Providers / External World

New capabilities should connect to this architecture instead of creating
parallel execution paths.

Current Architectural Direction

The immediate architectural priority is integration.

The objective is to connect the existing NEXA subsystems into a coherent
end-to-end system while preserving:

Modularity
Testability
Security
Governance
Clear interfaces
Provider independence
Fail-closed execution
Upgradeability

NEXA should grow by strengthening the connections between its existing
systems rather than continually creating isolated subsystems.