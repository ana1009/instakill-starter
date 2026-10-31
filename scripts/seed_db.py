"""Seeds the InstaKill database with a handful of synthetic users and posts."""
from app.db.database import get_connection, init_db

USERS = ["alice", "bob", "carol", "dave", "erin"]
POSTS = [
    (1, "hello world, this is my first post"),
    (1, "does anyone else think the feed is chronological only? boring"),
    (2, "just shipped a cosine similarity search, feels great"),
    (3, "spam spam spam buy now click here"),
    (4, "benchmarking my ranker against popularity baseline today"),
    (5, "red-team week is going to be brutal, good luck everyone"),
]
# (follower_id, followed_id)
# 1=alice, 2=bob, 3=carol, 4=dave, 5=erin
FOLLOWS = [
    (1, 2),  # alice follows bob
    (1, 4),  # alice follows dave
    (2, 5),  # bob follows erin
    (4, 2),  # dave follows bob
    (5, 1),  # erin follows alice
]
# (user_id, post_id)
LIKES = [
    (1, 3),  # alice likes post 3
    (2, 3),  # bob likes post 3
    (4, 3),  # dave likes post 3 (makes post 3 popular)
    (5, 1),  # erin likes post 1
    (2, 5),  # bob likes post 5
]

def seed() -> None:
    init_db()
    with get_connection() as conn:
        for username in USERS:
            conn.execute(
                "INSERT OR IGNORE INTO user (username) VALUES (?)", (username,)
            )
        for user_id, content in POSTS:
            conn.execute(
                "INSERT INTO post (user_id, content) VALUES (?, ?)", (user_id, content)
            )
        for follower_id, followed_id in FOLLOWS:
            conn.execute(
                "INSERT OR IGNORE INTO user_follow (follower_id, followed_id) VALUES (?, ?)",
                (follower_id, followed_id)
            )
        for user_id, post_id in LIKES:
            conn.execute(
                "INSERT OR IGNORE INTO user_like (user_id, post_id) VALUES (?, ?)",
                (user_id, post_id)
            )
        conn.commit()
    print(f"Seeded {len(USERS)} users, {len(POSTS)} posts, {len(FOLLOWS)} follows, and {len(LIKES)} likes.")


if __name__ == "__main__":
    seed()
