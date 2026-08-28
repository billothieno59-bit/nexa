import pytest
from core.cognition.memory.adapters.vector_adapter import SimpleVectorAdapter


@pytest.fixture
def vector_adapter():
    return SimpleVectorAdapter()


def test_vector_upsert_and_search(vector_adapter):
    v1 = [1.0, 0.0, 0.0]
    v2 = [0.0, 1.0, 0.0]

    vector_adapter.upsert("doc1", v1, {"text": "apple"})
    vector_adapter.upsert("doc2", v2, {"text": "banana"})

    query = [0.9, 0.1, 0.0]
    results = vector_adapter.search(query, top_k=1)

    assert len(results) == 1
    assert results[0]["id"] == "doc1"
    assert results[0]["metadata"]["text"] == "apple"
