# API Contract: Create Post

**Endpoint:** `POST /posts/`
**Description:** Creates a new post associated with an existing user.

### Request Body (application/json)
```json
{
  "author_id": 1,
  "content": "My first post on InstaKill!",
  "image_url": "https://example.com/photo.jpg"
}
```

### Successful Response (201 Created)
```json
{
  "id": 12,
  "author_id": 1,
  "content": "My first post on InstaKill!",
  "image_url": "https://example.com/photo.jpg",
  "created_at": "2026-10-24T14:30:00Z"
}
```

### Expected Validation & Error Cases
* **422 Unprocessable Entity:** Returned if required fields are missing (e.g., `author_id` or `content`) or if the data types are incorrect (e.g., string instead of integer for ID).
* **404 Not Found:** Returned if the `author_id` does not exist in the database.