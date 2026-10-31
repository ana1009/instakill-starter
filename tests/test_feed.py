from app.services.feed_ranker import rank_feed


def test_rank_feed_determinism_and_tie_break():
    """Tests if rank_feed sorts correctly, resolves ties, and does not mutate inputs."""
    candidates = [
        {"post_id": 3, "user_id": 2, "content": "A", "created_at": 1000},
        {"post_id": 1, "user_id": 2, "content": "B", "created_at": 1000},  # Tie with post 3
        {"post_id": 2, "user_id": 3, "content": "C", "created_at": 500},
    ]

    signals = {"followed_authors": {2}, "post_likes": {1: 10, 3: 10}}
    weights = {"freshness": 0.0, "affinity": 1.0, "popularity": 0.0}  # Isolate affinity

    # Execute pure function
    results1 = rank_feed(candidates, signals, now=2000, weights=weights, limit=3)
    results2 = rank_feed(candidates, signals, now=2000, weights=weights, limit=3)

    # Determinism
    assert results1 == results2

    # Ordering and tie-breaker (post 1 before post 3 due to ascending post_id)
    assert len(results1) == 3
    assert results1[0]["post_id"] == 1
    assert results1[1]["post_id"] == 3
    assert results1[2]["post_id"] == 2

    # Mutation check: original list and dicts must lack the "score" key
    assert "score" not in candidates[0]