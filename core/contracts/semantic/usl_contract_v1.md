# NEXA African Operating System
# USL Semantic Contract v1.0

Status: Foundational Contract
Authority: CONSTITUTION.md
Canonical Universal: USL
Canonical Implementation: core/semantic/

## 1. Purpose

USL (Universal Semantic Layer) defines the language-independent semantic representation used by NEXA after communication has been interpreted.

USL exists to separate meaning from human language, dialect, presentation language, and communication modality.

## 2. Core Principle

Human language is not the foundation of cognition.

UCL converts human communication into semantic meaning.

USL represents that meaning in a language-independent form suitable for downstream cognition.

The canonical flow is:

Human Communication
        ↓
       UCL
        ↓
       USL
        ↓
    Cognition

## 3. Responsibility

USL is responsible for representing:

- semantic meaning
- entities
- relationships
- actions
- properties
- intent
- constraints
- temporal information
- spatial information
- quantities
- references
- uncertainty
- relevant communication context

USL must preserve meaning required by downstream reasoning.

## 4. Language Independence

USL must not require cognition to operate directly on:

- English
- Kiswahili
- Sheng
- other natural languages
- dialect-specific surface forms
- presentation-specific wording

Different human-language inputs expressing equivalent meaning should be capable of producing equivalent semantic representations.

## 5. Input Boundary

USL receives normalized communication representations from UCL.

USL may receive:

- normalized text
- speech-derived meaning
- language and dialect metadata
- communication context
- detected intent
- entities
- references
- uncertainty information

USL must not assume that the source language is the internal reasoning language.

## 6. Semantic Representation

A USL representation should describe what the user means rather than merely reproducing what the user said.

Semantic representations may contain:

- actors
- objects
- actions
- states
- relationships
- goals
- constraints
- events
- time
- location
- quantities
- confidence
- ambiguity

## 7. Ambiguity and Uncertainty

USL must preserve meaningful ambiguity when the available communication does not provide enough information to resolve it.

USL must not silently invent facts to complete an incomplete meaning representation.

Where appropriate, uncertainty and confidence must remain explicit.

## 8. Context

USL may incorporate relevant context required to interpret meaning.

Context may include:

- conversation context
- references to previous statements
- user-provided constraints
- temporal context
- spatial context
- communication context

Context must not be used to bypass subsystem ownership or trust boundaries.

## 9. Cognition Boundary

USL must not own:

- long-term reasoning
- planning
- decision authority
- execution
- orchestration
- trust authority
- policy authority

Those responsibilities belong to their canonical subsystems.

USL represents meaning; cognition reasons over meaning.

## 10. Output Boundary

USL provides semantic representations to cognition and other authorized downstream subsystems.

Downstream systems must not be required to reconstruct the original human language in order to understand the semantic representation.

## 11. Presentation Independence

USL must remain independent of the language or modality used to present NEXA's response.

The same semantic result may subsequently be presented through:

- English
- Kiswahili
- Sheng
- another supported language
- text
- speech
- visual interfaces
- accessibility interfaces

Presentation is outside the semantic foundation.

## 12. Replaceability

The USL contract is authoritative.

Multiple semantic representation implementations may exist beneath:

core/semantic/

Implementations may change without changing the contract.

## 13. Constitutional Requirement

Every USL implementation must preserve:

1. language independence of cognition
2. semantic preservation
3. explicit uncertainty
4. contextual meaning
5. presentation independence
6. canonical module ownership
7. replaceability
8. explicit boundary between semantic representation and cognition

## 14. Architecture Rule

USL must remain a semantic boundary between communication and cognition.

Communication representations belong to UCL.

Semantic representations belong to USL.

Reasoning and decision processes belong to Cognition.

No subsystem may silently absorb another subsystem's canonical responsibility.
