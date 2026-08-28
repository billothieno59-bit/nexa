from typing import Any, Dict, Optional
from core.cognition.memory.manager import MemoryManager
from core.cognition.routing.router import SemanticRouter
from core.cognition.execution.pipeline import ExecutionPipeline


class AgentContext:
    """Orchestrates memory, intent routing, and step pipelines for an agent session."""

    def __init__(
        self,
        agent_id: str,
        memory_manager: Optional[MemoryManager] = None,
        router: Optional[SemanticRouter] = None,
    ):
        self.agent_id = agent_id
        self.memory = memory_manager or MemoryManager()
        self.router = router or SemanticRouter()
        self.pipeline = ExecutionPipeline()

    def load_session(self, session_id: str) -> Dict[str, Any]:
        data = self.memory.retrieve_memory(session_id)
        return data or {"session_id": session_id, "agent_id": self.agent_id}

    def save_session(self, session_id: str, payload: Dict[str, Any]) -> bool:
        return self.memory.store_memory(session_id, payload)

    def execute_intent(self, intent: str, **kwargs) -> Any:
        return self.router.dispatch(intent, **kwargs)
