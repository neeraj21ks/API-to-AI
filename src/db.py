import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_db_connection() -> psycopg.Connection:
    """Create a PostgreSQL connection using DATABASE_URL.

    The caller owns the connection and must close it (preferably with a
    context manager). No connection is opened at import time.
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not configured. Copy .env.example to .env "
            "and set the local PostgreSQL credentials."
        )
    return psycopg.connect(database_url)
