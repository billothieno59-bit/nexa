from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import List


CANONICAL_PIPELINE = [
    "Decision",
    "Planner",
    "Orchestrator",
    "Dispatcher",
    "Authorization",
    "Executor",
]


@dataclass
class PipelineState:
    stages: List[str] = field(default_factory=lambda: CANONICAL_PIPELINE.copy())
    current_index: int = 0
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    def current_stage(self) -> str:
        return self.stages[self.current_index]

    def next(self) -> str:
        if self.current_index < len(self.stages) - 1:
            self.current_index += 1
        self.updated_at = datetime.now(UTC)
        return self.current_stage

    def reset(self) -> None:
        self.current_index = 0
        self.updated_at = datetime.now(UTC)

    def snapshot(self) -> dict:
        return {
            "current_stage": self.current_stage,
            "current_index": self.current_index,
            "stages": self.stages,
            "updated_at": self.updated_at.isoformat(),
        }


PIPELINE_STATE = PipelineState()
