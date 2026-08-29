
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass
class ProviderState:
    name: str
    connected: bool
    status: str


@dataclass
class SystemState:
    system: str = "NEXA"
    version: str = "3.2"
    phase: str = "Phase 3"
    started_at: datetime = field(default_factory=datetime.utcnow)

    providers: Dict[str, ProviderState] = field(default_factory=dict)
    pipeline: List[str] = field(default_factory=lambda: [
        "Decision",
        "Planner",
        "Orchestrator",
        "Dispatcher",
        "Authorization",
        "Executor",
    ])

    active_stage: str = "Decision"

    def register_provider(self, key: str, name: str, connected: bool, status: str) -> None:
        self.providers[key] = ProviderState(
            name=name,
            connected=connected,
            status=status,
        )

    def set_stage(self, stage: str) -> None:
        if stage not in self.pipeline:
            raise ValueError(f"Unknown pipeline stage: {stage}")
        self.active_stage = stage

    def snapshot(self) -> dict:
        return {
            "system": self.system,
            "version": self.version,
            "phase": self.phase,
            "active_stage": self.active_stage,
            "pipeline": self.pipeline,
            "providers": {
                key: {
                    "name": value.name,
                    "connected": value.connected,
                    "status": value.status,
                }
                for key, value in self.providers.items()
            },
        }


SYSTEM_STATE = SystemState()

SYSTEM_STATE.register_provider(
    "reasoning",
    "Anthropic",
    True,
    "connected",
)

SYSTEM_STATE.register_provider(
    "image",
    "OpenAI",
    True,
    "connected",
)

SYSTEM_STATE.register_provider(
    "voice",
    "ElevenLabs",
    True,
    "connected",
)

SYSTEM_STATE.register_provider(
    "local",
    "NEXA Local",
    False,
    "reserved",
)
