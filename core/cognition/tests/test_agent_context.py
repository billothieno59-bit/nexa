import pytest
from core.cognition.agent_context import AgentContext
from core.cognition.memory.manager import MemoryManager
from core.cognition.memory.adapters.sqlite_adapter import SQLiteMemoryAdapter


@pytest.fixture
def agent(tmp_path):
    db_file = tmp_path / "agent_test.db"
    adapter = SQLiteMemoryAdapter(db_path=str(db_file))
    memory_manager = MemoryManager(adapter=adapter)
    return AgentContext(agent_id="agent_alpha", memory_manager=memory_manager)


def test_agent_session_lifecycle(agent):
    session_data = {"session_id": "s_100", "status": "active"}
    assert agent.save_session("s_100", session_data) is True

    loaded = agent.load_session("s_100")
    assert loaded["session_id"] == "s_100"
    assert loaded["status"] == "active"


def test_agent_intent_dispatch(agent):
    agent.router.register("ping", lambda: "pong")
    assert agent.execute_intent("ping") == "pong"
