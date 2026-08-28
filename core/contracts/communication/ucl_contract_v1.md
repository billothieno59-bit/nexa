# NEXA African Operating System
# UCL Communication Contract v1.0

Status: Foundational Contract
Authority: CONSTITUTION.md
Canonical Universal: UCL
Canonical Implementation: core/interaction/communication/

## 1. Purpose

UCL (Universal Communication Layer) defines the contract for communication between humans and NEXA.

UCL is responsible for representing human communication without making any
human language the foundation of cognition.

## 2. Supported Communication

UCL must be capable of representing:

- natural languages
- African languages
- dialects
- Sheng
- code-switching
- text
- speech
- language identification
- communication context
- translation
- response-language preference

Actual language coverage depends on the implementations and models connected
to the contract.

## 3. Core Principle

Human language is an external communication representation.

It is not the internal representation used by cognition.

The canonical flow is:

Human Communication
        ↓
       UCL
        ↓
     Semantic
     Meaning
        ↓
      Cognition

## 4. Input Contract

UCL receives a communication request containing, where available:

- content
- modality
- detected language
- dialect
- communication context
- speaker information
- confidence
- code-switching information
- user language preference

## 5. Output Contract

UCL produces a normalized communication representation suitable for semantic
interpretation.

The representation must preserve meaning and relevant linguistic or cultural
context without requiring downstream cognition to operate in the source language.

## 6. Code-Switching

Code-switching is a first-class communication capability.

A single communication request may contain multiple languages or dialects.

Example:

English + Sheng + Kiswahili
        ↓
UCL
        ↓
Unified semantic interpretation

The system must not require the user to manually identify every language.

## 7. Dialects and Local Languages

Dialect and local-language information may carry semantic or cultural meaning.

UCL must preserve relevant distinctions rather than automatically discarding
them through generic translation.

## 8. Response Language

NEXA must be capable of selecting an appropriate response language based on:

- explicit user preference
- detected communication language
- conversation context
- user identity preferences
- accessibility requirements
- system policy

## 9. Semantic Boundary

UCL must not contain:

- core reasoning
- long-term knowledge reasoning
- planning
- orchestration
- execution authority
- trust authority

Those responsibilities belong to their canonical subsystems.

## 10. Implementation Boundary

The contract is authoritative.

Multiple implementations may exist beneath:

core/interaction/communication/

Implementations may change without changing this contract.

## 11. Constitutional Requirement

Every UCL implementation must preserve:

1. language independence of cognition
2. dialect awareness
3. code-switching support
4. semantic preservation
5. replaceability
6. canonical module ownership
7. explicit boundaries between communication and cognition
