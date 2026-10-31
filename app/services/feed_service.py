import time
from typing import Dict, Any
from app.db import database
from app.services.feed_ranker import rank_feed, rank_chronological


def build_feed(user_id: int, limit: int, strategy: str) -> Dict[str, Any]:
    """Orchestrates data fetching and ranking for the feed."""
    if not database.check_user_exists(user_id):
        return None  # Handled as 404 in the API edge

    liked_ids = database.get_user_liked_post_ids(user_id)
    all_posts = database.get_feed_candidates()

    candidates = [p for p in all_posts if p["user_id"] != user_id and p["post_id"] not in liked_ids]

    if strategy == "chronological":
        results = rank_chronological(candidates, limit)
        return {"user_id": user_id, "strategy": strategy, "results": results}

    signals = {
        "followed_authors": database.get_user_followed_authors(user_id),
        "post_likes": database.get_global_post_likes()
    }
    weights = {"freshness": 1.0, "affinity": 2.0, "popularity": 1.0}
    now = int(time.time())

    results = rank_feed(candidates, signals, now, weights, limit)
    return {"user_id": user_id, "strategy": strategy, "results": results}