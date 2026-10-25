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