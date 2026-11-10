"""Environment configuration helpers.

Application code should read secrets from environment variables and must never
print credential values to logs.
"""

import os

from dotenv import load_dotenv

load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def valid_config() -> None:
    get_required_env("DATABASE_URL")
