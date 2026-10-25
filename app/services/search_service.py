import numpy as np
from typing import List, Dict, Any


def cosine_similarity(query_vector: np.ndarray, corpus_vectors: np.ndarray) -> np.ndarray:
    """Calculates cosine similarity, safely handling zero vectors."""
    norm_q = np.linalg.norm(query_vector)
    norm_c = np.linalg.norm(corpus_vectors, axis=1)

    norm_q = norm_q if norm_q > 0 else 1.0
    norm_c = np.where(norm_c > 0, norm_c, 1.0)

    return np.dot(corpus_vectors, query_vector) / (norm_c * norm_q)


def stable_top_k(scores: np.ndarray, post_ids: np.ndarray, limit: int) -> np.ndarray:
    """Returns indices ordered by score descending, then post_id ascending."""
    sort_indices = np.lexsort((post_ids, -scores))
    return sort_indices[:limit]


def semantic_search(query_vector: np.ndarray, posts: List[Dict[str, Any]], corpus_vectors: np.ndarray, limit: int) -> \
List[Dict[str, Any]]:
    """Returns the top search results ordered by relevance."""
    if not posts or len(corpus_vectors) == 0:
        return []

    scores = cosine_similarity(query_vector, corpus_vectors)
    post_ids = np.array([p["post_id"] for p in posts])

    top_indices = stable_top_k(scores, post_ids, limit)

    results = []
    for idx in top_indices:
        results.append({
            "post_id": posts[idx]["post_id"],
            "user_id": posts[idx]["user_id"],
            "content": posts[idx]["content"],
            "score": float(scores[idx])
        })

    return results