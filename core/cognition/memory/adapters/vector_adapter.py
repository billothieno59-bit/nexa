import math
from typing import Any, Dict, List, Tuple


class SimpleVectorAdapter:
    """Lightweight vector similarity adapter using cosine similarity."""

    def __init__(self):
        self._index: Dict[str, Tuple[List[float], Dict[str, Any]]] = {}

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))
        if not magnitude1 or not magnitude2:
            return 0.0
        return dot_product / (magnitude1 * magnitude2)

    def upsert(self, vector_id: str, vector: List[float], metadata: Dict[str, Any]) -> bool:
        self._index[vector_id] = (vector, metadata)
        return True

    def search(self, query_vector: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        results = []
        for vec_id, (vec, meta) in self._index.items():
            score = self._cosine_similarity(query_vector, vec)
            results.append({"id": vec_id, "score": score, "metadata": meta})

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
