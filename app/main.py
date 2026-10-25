import sqlite3
import numpy as np
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query

from app.db.database import init_db
from app.adapters.encoder import encoder
from app.services.search_service import semantic_search

app_state = {
    "posts": [],
    "corpus_embeddings": np.array([])
}


def get_seeded_posts_from_db():
    """
    Fetches all existing posts directly from the SQLite database.
    Assumes the database file is named 'instakill.db' at the project root.
    """
    with sqlite3.connect("instakill.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Adjust column names if your schema differs (e.g., id vs post_id)
        cursor.execute("SELECT id AS post_id, user_id AS user_id, content FROM post")
        return [dict(row) for row in cursor.fetchall()]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database from existing code
    init_db()

    # Build the semantic in-memory index at startup
    posts = get_seeded_posts_from_db()
    if posts:
        texts = [p["content"] for p in posts]
        app_state["corpus_embeddings"] = encoder.encode(texts)
        app_state["posts"] = posts

    yield
    app_state.clear()


app = FastAPI(title="InstaKill", lifespan=lifespan)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/search")
def search_posts(q: str = Query(..., min_length=1), limit: int = Query(5, ge=1, le=20)):
    """Semantic search endpoint returning ordered top results."""
    if not app_state["posts"]:
        return {"query": q, "results": []}

    query_vector = encoder.encode([q])[0]
    results = semantic_search(
        query_vector=query_vector,
        posts=app_state["posts"],
        corpus_vectors=app_state["corpus_embeddings"],
        limit=limit
    )

    return {
        "query": q,
        "results": results
    }