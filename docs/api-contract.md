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

### `GET /feed`
Generates a feed of posts for a specific user, sorted either by a personalized ranking algorithm or strictly chronologically.

**Query Parameters:**
- `user_id` (integer, required): The ID of the user requesting the feed.
- `limit` (integer, optional): The maximum number of posts to return. Must be between 1 and 50. Default is 20.
- `strategy` (string, optional): The ranking strategy to use. Must be either `for_you` or `chronological`. Default is `for_you`.

**Response Formats:**
- **200 OK**: Successfully generated the feed.
  ```json
  {
    "user_id": 1,
    "strategy": "for_you",
    "results": [
      {
        "post_id": 27,
        "user_id": 2,
        "content": "just shipped a cosine similarity search, feels great",
        "created_at": 1793450181,
        "score": 2.9594882729211087
      },
      {
        "post_id": 29,
        "user_id": 4,
        "content": "benchmarking my ranker against popularity baseline today",
        "created_at": 1793450181,
        "score": 2.9594882729211087
      }
    ]
  }
  
(Note: The score field is only present when strategy="for_you". Ties in score or timestamp are broken deterministically by ascending post_id.)

404 Not Found: The provided user_id does not exist in the database.

422 Unprocessable Entity: Validation error (e.g., limit is out of bounds or strategy is unrecognized).