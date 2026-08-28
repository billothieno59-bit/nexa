import pytest
from core.cognition.memory.manager import MemoryManager
from core.cognition.memory.adapters.sqlite_adapter import SQLiteMemoryAdapter


@pytest.fixture
def memory_manager(tmp_path):
    db_file = tmp_path / "manager_test.db"
    adapter = SQLiteMemoryAdapter(db_path=str(db_file))
    return MemoryManager(adapter=adapter)


def test_manager_lifecycle(memory_manager):
    payload = {"context": "user_session", "token_count": 128}

    # Store
    assert memory_manager.store_memory("session_001", payload) is True

    # Retrieve
    retrieved = memory_manager.retrieve_memory("session_001")
    assert retrieved == payload

    # List
    all_memories = memory_manager.list_memories()
    assert len(all_memories) == 1

    # Forget
    assert memory_manager.forget_memory("session_001") is True
    assert memory_manager.retrieve_memory("session_001") is None
