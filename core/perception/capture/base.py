"""
NEXA Africa Operating System
File: core/perception/capture/base.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Abstract interface every perception capturer must implement,
             per core/contracts/perception/upl_contract_v1.md.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from core.perception.events import PerceptionEvent


class PerceptionCapturer(ABC):
    """
    Common interface for all perception capturers.

    A capturer's only job is turning raw input for one modality into a
    validated PerceptionEvent. It must not interpret meaning.
    """

    @property
    @abstractmethod
    def modality(self) -> str:
        """The modality this capturer produces events for (e.g. 'text')."""
        raise NotImplementedError

    @abstractmethod
    def capture(self, raw_input: object, source: str) -> PerceptionEvent:
        """
        Convert raw input into a structured PerceptionEvent.
        """
        raise NotImplementedError


__all__ = [
    "PerceptionCapturer",
]
