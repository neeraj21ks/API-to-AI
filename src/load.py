from collections.abc import Iterable
from typing import Any

from psycopg import Connection
from psycopg.types.json import Jsonb

from src.db import get_db_connection


def load_raw_event(
    batch_id: str,
    source: str,
    symbol: str,
    interval: str,
    payload: Any,
    ingested_at,
) -> None:
    """Persist the original API response for replay and investigation."""
    sql = """
        INSERT INTO raw_events (
            batch_id, source, symbol, interval, payload, ingested_at
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql,
                (batch_id, source, symbol, interval, Jsonb(payload), ingested_at),
            )


def _insert_clean_events(clean: Iterable[dict], conn: Connection) -> int:
    sql = """
        INSERT INTO clean_events (
            symbol, interval, open_time, close_time,
            open, high, low, close, volume,
            source, batch_id, ingested_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (symbol, interval, open_time) DO NOTHING
    """
    inserted = 0
    with conn.cursor() as cur:
        for record in clean:
            cur.execute(
                sql,
                (
                    record["symbol"],
                    record["interval"],
                    record["open_time"],
                    record["close_time"],
                    record["open"],
                    record["high"],
                    record["low"],
                    record["close"],
                    record["volume"],
                    record["source"],
                    record["batch_id"],
                    record["ingested_at"],
                ),
            )
            inserted += max(cur.rowcount, 0)
    return inserted


def load_clean_events(clean: Iterable[dict], conn: Connection | None = None) -> int:
    """Load validated records and return inserted-row count.

    Pass an existing connection to participate in its transaction. If no
    connection is supplied, this function owns a short-lived connection.
    Database errors deliberately propagate to the pipeline orchestrator.
    """
    if conn is not None:
        return _insert_clean_events(clean, conn)

    with get_db_connection() as owned_conn:
        return _insert_clean_events(clean, owned_conn)


def create_batch(batch_id: str, source: str, started_at) -> None:
    sql = """
        INSERT INTO pipeline_batches (batch_id, source, started_at, status)
        VALUES (%s, %s, %s, 'RUNNING')
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (batch_id, source, started_at))


def update_batch_status(
    batch_id: str,
    status: str,
    completed_at=None,
    records_extracted: int = 0,
    records_loaded: int = 0,
    records_quarantined: int = 0,
    error_message: str | None = None,
) -> None:
    allowed_statuses = {"RUNNING", "SUCCESS", "FAILED"}
    if status not in allowed_statuses:
        raise ValueError(f"Unsupported batch status: {status}")

    sql = """
        UPDATE pipeline_batches
        SET status = %s,
            completed_at = %s,
            records_extracted = %s,
            records_loaded = %s,
            records_quarantined = %s,
            error_message = %s
        WHERE batch_id = %s
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql,
                (
                    status,
                    completed_at,
                    records_extracted,
                    records_loaded,
                    records_quarantined,
                    error_message,
                    batch_id,
                ),
            )
            if cur.rowcount != 1:
                raise ValueError(f"Pipeline batch not found: {batch_id}")
