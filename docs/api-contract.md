# API Contract

## 1. Create Post

**Endpoint:** `POST /posts/`
**Description:** Creates a new post associated with an existing user.

### Request Body (application/json)

```
{
  "author_id": 1,
  "content": "My first post on InstaKill!",
  "image_url": "https://example.com/photo.jpg"
}

```

### Successful Response (201 Created)

```
{
  "id": 12,
  "author_id": 1,
  "content": "My first post on InstaKill!",
  "image_url": "https://example.com/photo.jpg",
  "created_at": "2026-10-24T14:30:00Z"
}

```

### Expected Validation & Error Cases

* **422 Unprocessable Entity:** Returned if required fields are missing (e.g., `author_id` or `content`) or if the data types are incorrect.

* **404 Not Found:** Returned if the `author_id` does not exist in the database.

## 2. Semantic Search

**Endpoint:** `GET /search`
**Description:** Performs semantic search over seeded posts.

### Query Parameters

* `q` (string, required): The search query. Cannot be empty.

* `limit` (integer, optional): Maximum number of results to return (1-20). Defaults to 5.

### Successful Response (200 OK)

```
{
  "query": "cheap dinner",
  "results": [
    {
      "post_id": 2,
      "user_id": 2,
      "content": "Looking for a cheap dinner tonight.",
      "score": 0.8521
    }
  ]
}

```

### Expected Validation & Error Cases

* **422 Unprocessable Entity:** Returned automatically by FastAPI if `q` is missing/empty, or if `limit` is outside the 1..20 range.