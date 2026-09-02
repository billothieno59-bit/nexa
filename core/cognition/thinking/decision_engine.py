"""
NEXA Decision Engine

Purpose:
    Convert validated semantic requests into a safe decision.

Architectural boundary:
    USL/semantic input -> Decision Engine -> Execution Planner

The Decision Engine does not execute actions.
It decides whether an interpreted request is:
    - informational
    - blocked
    - confirmation_required

This module must remain deterministic and side-effect free.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Decision:
    """
    Represents a canonical cognitive decision.

    A Decision is a structured, immutable description of how the
    system should treat a piece of interpreted input. It does not
    perform any action itself.
    """

    decision_type: str
    intent: str
    confidence: float
    requires_confirmation: bool
    reason: str = ""


class DecisionEngine:
    """
    Converts an interpreted intent into a canonical Decision.

    The engine is intentionally conservative: low-confidence or
    ambiguous input defaults toward confirmation_required rather
    than informational, and unknown or malformed input fails closed
    as blocked.
    """

    CONFIDENCE_THRESHOLD = 0.85

    BLOCKED_INTENTS = {
        "malicious",
        "unauthorized",
        "unknown",
    }

    def decide(
        self,
        intent: str,
        confidence: float,
    ) -> Decision:
        """
        Produce a Decision from an intent and its confidence score.
        Malformed confidence (non-numeric, bool, NaN, infinite, or
        outside [0, 1]) fails closed as blocked rather than being
        compared as-is.
        """

        if (
            not isinstance(confidence, (int, float))
            or isinstance(confidence, bool)
            or not math.isfinite(float(confidence))
            or not 0.0 <= float(confidence) <= 1.0
        ):
            return Decision(
                decision_type="blocked",
                intent="unknown" if not isinstance(intent, str) else (intent.strip() or "unknown"),
                confidence=0.0,
                requires_confirmation=False,
                reason="Invalid confidence. Expected a finite number between 0 and 1.",
            )

        if not isinstance(intent, str) or not intent.strip():
            return Decision(
                decision_type="blocked",
                intent="unknown",
                confidence=0.0,
                requires_confirmation=False,
                reason="Empty or invalid intent.",
            )

        cleaned_intent = intent.strip()

        if cleaned_intent in self.BLOCKED_INTENTS:
            return Decision(
                decision_type="blocked",
                intent=cleaned_intent,
                confidence=float(confidence),
                requires_confirmation=False,
                reason="Intent is explicitly blocked.",
            )

        if float(confidence) < self.CONFIDENCE_THRESHOLD:
            return Decision(
                decision_type="confirmation_required",
                intent=cleaned_intent,
                confidence=float(confidence),
                requires_confirmation=True,
                reason="Confidence below threshold.",
            )

        return Decision(
            decision_type="informational",
            intent=cleaned_intent,
            confidence=float(confidence),
            requires_confirmation=False,
            reason="No external side effect.",
        )


__all__ = [
    "Decision",
    "DecisionEngine",
]
