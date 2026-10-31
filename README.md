# InstaKill — Starter Repo

Mini social-media platform. Mandatory backend: Python + FastAPI + SQLite (default) / PostgreSQL (allowed). See the full brief and grading rubric in `masterplan.md` (course root).

What the instructor provides (this starter):

- `app/main.py` — FastAPI hello-world with `GET /health`
- `app/db/database.py` — SQLite bootstrap (creates tables on startup)
- `app/domain/models.py` — `User` / `Post` schema
- `scripts/seed_db.py` — 5-10 synthetic users/posts
- `tests/test_health.py` — test skeleton

What it does **not** provide: the feed, ranking, ML models, search. Those are the team's work, in the following weeks.

## Running it

```bash
pip install -e .
uvicorn app.main:app --reload
# other terminal:
curl localhost:8000/health

python scripts/seed_db.py
pytest
```

## Milestones (see masterplan.md for full details)

W1 Repo+API → W3 CRUD+DB → W4 Feed v0 → W7 Baseline+eval plan → W9 ML+pretrained feature → W11 Profile+optimize → W13 Feature freeze+E2E → W14 Red-team+Demo Day.

At the end of each week: a demonstrable commit/tag.

### Semantic Search Architecture

The search functionality uses a pure NumPy retrieval implementation and an in-memory index to ensure fast semantic matching without relying on external vector databases. 

**Index Initialization:** 
The in-memory index is built automatically at application startup using a FastAPI `lifespan` event (`app/main.py`). During this event, all seeded posts are fetched directly from the SQLite repository, and their contents are encoded into a NumPy matrix using the local `all-MiniLM-L6-v2` SentenceTransformer adapter.

**Index Refresh Strategy:**
Currently, the index loads only once at startup. To support new posts created by users in the future, the application will need a refresh mechanism. This could be achieved by either dynamically appending the new post's embedding to the in-memory `app_state["corpus_embeddings"]` matrix upon a successful `POST /posts/` request, or by scheduling a background task to rebuild the entire index periodically without blocking the main event loop.

## Feed Algorithm & Complexity

### Feed Strategy & Signals
The `GET /feed` endpoint provides a personalized `for_you` strategy using three ranking signals:
- **Freshness**: Uses an inverse decay formula `1.0 / (1.0 + (age_seconds / 3600.0))` to slightly favor newer posts.
- **Affinity**: Yields `1.0` if the post author is in the user's `followed_authors` set, otherwise `0.0`.
- **Popularity**: Evaluates `post_likes / max_global_likes` to boost globally appreciated content.
- **Default Weights**: `{freshness: 1.0, affinity: 2.0, popularity: 1.0}`.

### Candidates & Cold Start
- **Candidates**: The feed considers all posts from the database *except* the user's own posts and the posts the user has already liked.
- **Cold Start**: A user who follows nobody will have an empty affinity set. Their feed will naturally fall back to being ranked entirely by a combination of `freshness` and `popularity`, effectively acting as a "Trending" or "Latest Hits" feed.

### Complexity Note
The Big-O time complexity of a single `GET /feed` request is **`O(C log k)`**, where `C` is the number of valid candidate posts evaluated and `k` is the requested limit. This is achieved by using a min-heap (`heapq.nsmallest`) to strictly maintain only the top `k` items in memory during the scoring loop. 

**Optimization Strategy**: To improve performance at scale, I would precalculate the `freshness` and `popularity` scores asynchronously in a background job (or store them as materialized views), since these two signals are identical for all users. The API would then only need to calculate the personalized `affinity` dynamically at request time.