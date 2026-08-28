# NEXA African Operating System
# USL Semantic Representation Contract v1.0

Status: Foundational Schema
Authority: core/contracts/semantic/usl_contract_v1.md
Canonical Universal: USL
Canonical Schema: core/semantic/schema/

## 1. Purpose

This document defines the canonical structure of a USL semantic representation.

The representation describes meaning independently of human language,
presentation language, and communication modality.

## 2. Canonical Flow

Human Communication
        ↓
       UCL
        ↓
   USL Representation
        ↓
     Cognition

## 3. Required Top-Level Fields

Every USL representation must contain:

- schema_version
- request_id
- semantic_intent
- actors
- entities
- actions
- constraints
- context
- uncertainty

## 4. Schema Version

schema_version identifies the version of the USL representation contract.

Example:

schema_version: "1.0"

Implementations must not silently reinterpret a representation according to
an incompatible schema version.

## 5. Request Identity

request_id uniquely identifies the semantic interpretation request.

It is used for tracing and correlation.

It must not itself contain semantic meaning.

## 6. Semantic Intent

semantic_intent represents the primary intended purpose of the communication.

Examples include:

- request_information
- request_action
- provide_information
- ask_question
- express_preference
- report_event
- issue_command
- unknown

Intent classification must preserve uncertainty when intent cannot be
reliably determined.

## 7. Actors

actors represent participants relevant to the meaning.

An actor may represent:

- the user
- NEXA
- another person
- an organization
- a system
- an unknown participant

Actor identity must not be invented when it is unavailable.

## 8. Entities

entities represent meaningful objects, concepts, places, people, systems,
or other references contained in the communication.

Each entity may contain:

- entity_id
- entity_type
- label
- attributes
- references
- confidence

The original human-language label may be preserved as metadata but must not
be required for semantic reasoning.

## 9. Actions

actions represent events or activities expressed or implied by the communication.

Each action may contain:

- action_id
- action_type
- actor
- target
- parameters
- temporal_information
- spatial_information
- confidence

Actions must distinguish between what is explicitly stated and what is
inferred.

## 10. Constraints

constraints represent conditions that affect interpretation or downstream
reasoning.

Examples include:

- time constraints
- location constraints
- quantity constraints
- user preferences
- accessibility requirements
- required outputs
- exclusions

Constraints must remain explicit.

## 11. Context

context contains information necessary to interpret the current meaning.

Context may include:

- conversation references
- previous statements
- temporal context
- spatial context
- communication context
- relevant user-provided context

Context must not be used to bypass trust, policy, or subsystem boundaries.

## 12. Uncertainty

uncertainty represents unresolved ambiguity or confidence.

It may contain:

- overall_confidence
- ambiguous_fields
- unresolved_references
- alternative_interpretations
- missing_information

USL must never silently convert uncertainty into certainty.

## 13. Semantic Preservation

The representation must preserve information necessary for downstream
reasoning.

Lossy normalization is prohibited when the removed information changes
meaning, intent, constraints, identity, or relevant cultural context.

## 14. Language Independence

USL representations must not require cognition to understand:

- English
- Kiswahili
- Sheng
- another natural language
- dialect-specific wording
- presentation-specific wording

Equivalent meanings expressed through different languages should be capable
of producing equivalent semantic structures.

## 15. Boundary

USL representations must not contain:

- reasoning conclusions presented as facts without provenance
- execution authority
- trust authority
- policy authority
- hidden system instructions
- implementation-specific control commands

USL represents meaning.

Cognition reasons over meaning.

Execution occurs elsewhere.

## 16. Provenance

Where information is inferred rather than explicitly communicated, the
representation should preserve provenance indicating that distinction.

Possible provenance values:

- explicit
- inferred
- contextual
- system_derived
- unknown

## 17. Replaceability

The canonical representation belongs to USL.

Different parsers, language models, speech systems, and semantic extraction
implementations may produce the representation.

Downstream cognition must depend on the contract rather than a specific
implementation.

## 18. Constitutional Requirement

Every USL representation must preserve:

1. language independence
2. semantic meaning
3. explicit uncertainty
4. contextual meaning
5. semantic provenance
6. constraint preservation
7. canonical ownership
8. replaceability
9. separation between meaning and reasoning

## 19. Canonical Principle

The USL representation describes:

"What does this communication mean?"

It does not describe:

"What should NEXA do?"

The first belongs to USL.

The second belongs to cognition and authorized downstream systems.
