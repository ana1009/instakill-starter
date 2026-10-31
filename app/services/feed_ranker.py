import heapq
from typing import List, Dict, Any


def rank_feed(candidates: List[Dict[str, Any]], signals: Dict[str, Any], now: int, weights: Dict[str, float],
              limit: int) -> List[Dict[str, Any]]:
    """Pure ranking function using a heap-based top-k algorithm."""
    scored = []
    followed_authors = signals.get("followed_authors", set())
    post_likes = signals.get("post_likes", {})
    max_likes = max(post_likes.values()) if post_likes else 1

    for post in candidates:
        age_seconds = max(0, now - post["created_at"])
        freshness_score = 1.0 / (1.0 + (age_seconds / 3600.0))
        affinity_score = 1.0 if post["user_id"] in followed_authors else 0.0
        popularity_score = post_likes.get(post["post_id"], 0) / max_likes

        score = (weights.get("freshness", 1.0) * freshness_score +
                 weights.get("affinity", 1.0) * affinity_score +
                 weights.get("popularity", 1.0) * popularity_score)

        scored.append((score, post["post_id"], post))

    best = heapq.nsmallest(limit, scored, key=lambda x: (-x[0], x[1]))

    results = []
    for score, _, post in best:
        result_post = post.copy()
        result_post["score"] = float(score)
        results.append(result_post)
    return results


def rank_chronological(candidates: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
    """Sorts candidates strictly by created_at descending."""
    best = heapq.nsmallest(limit, [(post["created_at"], post["post_id"], post) for post in candidates],
                           key=lambda x: (-x[0], x[1]))
    return [post.copy() for _, _, post in best]