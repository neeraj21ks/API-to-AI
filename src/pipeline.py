import logging
import uuid
from datetime import datetime, timezone

from src.db import get_db_connection
from src.extract import SYMBOLS, fetch_klines
from src.kline_process import process_klines
from src.load import (
    create_batch,
    load_clean_events,
    load_raw_event,
    update_batch_status,
)

logger = logging.getLogger(__name__)


def run_pipeline() -> str:
    """Run one auditable Binance-to-PostgreSQL batch."""
    batch_id = str(uuid.uuid4())
    started_at = datetime.now(timezone.utc)
    records_extracted = 0
    records_loaded = 0
    records_quarantined = 0
    conn = None

    logger.info("Starting pipeline batch_id=%s", batch_id)
    create_batch(batch_id=batch_id, source="binance", started_at=started_at)

    try:
        conn = get_db_connection()

        for symbol in SYMBOLS:
            data = fetch_klines(symbol=symbol, interval="1m", limit=10)
            if not data:
                logger.warning("No candle data returned for %s", symbol)
                continue

            records_extracted += len(data)
            ingested_at = datetime.now(timezone.utc)

            load_raw_event(
                batch_id=batch_id,
                source="binance",
                symbol=symbol,
                interval="1m",
                payload=data,
                ingested_at=ingested_at,
            )

            clean, quarantined = process_klines(
                symbol=symbol,
                raw_klines=data,
                interval="1m",
                batch_id=batch_id,
                ingested_at=ingested_at,
            )
            records_quarantined += len(quarantined)

            if clean:
                inserted = load_clean_events(clean, conn)
                records_loaded += inserted
                logger.info(
                    "%s: extracted=%d valid=%d inserted=%d quarantined=%d",
                    symbol,
                    len(data),
                    len(clean),
                    inserted,
                    len(quarantined),
                )

        conn.commit()
        completed_at = datetime.now(timezone.utc)
        update_batch_status(
            batch_id=batch_id,
            status="SUCCESS",
            completed_at=completed_at,
            records_extracted=records_extracted,
            records_loaded=records_loaded,
            records_quarantined=records_quarantined,
        )
        logger.info(
            "Pipeline batch succeeded batch_id=%s extracted=%d inserted=%d quarantined=%d",
            batch_id,
            records_extracted,
            records_loaded,
            records_quarantined,
        )
        return batch_id

    except Exception as err:
        if conn is not None:
            conn.rollback()

        logger.exception("Pipeline batch failed batch_id=%s", batch_id)
        update_batch_status(
            batch_id=batch_id,
            status="FAILED",
            completed_at=datetime.now(timezone.utc),
            records_extracted=records_extracted,
            records_loaded=records_loaded,
            records_quarantined=records_quarantined,
            error_message=str(err)[:4000],
        )
        raise

    finally:
        if conn is not None:
            conn.close()
