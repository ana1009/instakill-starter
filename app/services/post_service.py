from typing import Optional
from app.domain.models import Post


def create_new_post(author_id: int, content: str, image_url: Optional[str] = None) -> Post:
    """
        Coordinates the creation of a new post by validating data through the domain model.
        Does not interact directly with the database or HTTP requests.
    """
    new_post = Post(
        author_id=author_id,
        content=content,
        image_url=image_url
    )
    # A call to the repository layer for SQLite persistence will be added here later
    return new_post