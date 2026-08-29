# NEXA Architecture

## Overview

NEXA is a modular AI platform built around governed cognition, perception,
knowledge, identity, communication, execution, and trust.

## Core Flow

User
↓
Interface
↓
Application Layer
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

## Core Layers

- USL — Semantic Layer
- UCL — Communication Layer
- UAL — Accessibility Layer
- UPL — Perception Layer
- UKL — Knowledge Layer
- UIL — Identity Layer
- UOL — Orchestration Layer
- UML — Machine Interface Layer
- UTL — Trust Layer

## Interface

The web interface communicates with NEXA through the application/API layer.

The interface must not bypass governance or directly execute privileged actions.

## Cognition

Cognition is responsible for interpretation, reasoning, memory, context,
decision support, and routing.

## Execution

Execution follows the governed pipeline:

Decision
→ Planner
→ Orchestrator
→ Dispatcher
→ Authorization
→ Executor
→ Handler

## Security

NEXA follows fail-closed principles.

Blocked or unauthorized operations must never reach execution.

Identity and authorization are separate concerns.

## Testing

Every major subsystem should have automated tests.

The current baseline is:

364 tests passing.