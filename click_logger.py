import sqlite3
from datetime import datetime, timezone

DB_PATH = "clicks.db"

def logger(query, url, position):
    timestamp = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS clicks (
                timestamp TEXT,
                query TEXT,
                url TEXT,
                position INTEGER
            )
        """)

        conn.execute(
            """
            INSERT INTO clicks (timestamp, query, url, position)
            VALUES (?, ?, ?, ?)
            """,
            (timestamp, query, url, position)
        )
