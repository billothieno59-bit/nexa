import pytest
from core.cognition.memory.adapters.sqlite_adapter import SQLiteMemoryAdapter


@pytest.fixture
def memory_adapter(tmp_path):
    db_file = tmp_path / "test_memory.db"
    return SQLiteMemoryAdapter(db_path=str(db_file))


def test_save_and_get_entry(memory_adapter):
    data = {"agent": "jarvis", "task": "authorize_action", "status": "pending"}
    assert memory_adapter.save("task_001", data) is True
    retrieved = memory_adapter.get("task_001")
    assert retrieved == data


def test_update_existing_entry(memory_adapter):
    data = {"task": "initial"}
    memory_adapter.save("task_002", data)
    updated_data = {"task": "updated"}
    memory_adapter.save("task_002", updated_data)
    assert memory_adapter.get("task_002") == updated_data


def test_get_nonexistent_key(memory_adapter):
    assert memory_adapter.get("missing_key") is None


def test_delete_entry(memory_adapter):
    memory_adapter.save("task_003", {"data": "test"})
    assert memory_adapter.delete("task_003") is True
    assert memory_adapter.get("task_003") is None


def test_list_all_entries(memory_adapter):
    memory_adapter.save("k1", {"val": 1})
    memory_adapter.save("k2", {"val": 2})
    all_items = memory_adapter.list_all()
    assert len(all_items) == 2
    assert {"val": 1} in all_items
    assert {"val": 2} in all_items
