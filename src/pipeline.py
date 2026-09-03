import logging
import uuid

from datetime import datetime, timezone

from src.extract import fetch_klines, SYMBOLS
from src.kline_process import process_klines
from src.db import get_db_connection

from src.load import (
    load_raw_event,
    load_clean_events,
    create_batch,
    update_batch_status
)


logger = logging.getLogger(__name__)


def run_pipeline():

    # ---------------------------------------
    # CREATE BATCH
    # ---------------------------------------

    batch_id = str(uuid.uuid4())
    started_at = datetime.now(timezone.utc)
    ingested_at = started_at

    records_extracted = 0
    records_loaded = 0
    records_quarantined = 0

    logger.info(
        f"Starting pipeline batch | "
        f"batch_id={batch_id} | "
        f"ingested_at={ingested_at}"
    )

    # ---------------------------------------
    # REGISTER BATCH
    # ---------------------------------------

    create_batch(
        batch_id=batch_id,
        source="binance",
        started_at=started_at
    )

    # ---------------------------------------
    # DATABASE CONNECTION
    # ---------------------------------------

    conn = get_db_connection()

    try:

        # -----------------------------------
        # PROCESS EACH SYMBOL
        # -----------------------------------

        for symbol in SYMBOLS:

            data = fetch_klines(
                symbol=symbol,
                interval="1m",
                limit=10
            )

            # --------------------------------
            # EXTRACTION FAILURE
            # --------------------------------

            if data is None:

                logger.warning(
                    f"No data received for {symbol}"
                )

                continue

            # --------------------------------
            # COUNT EXTRACTED
            # --------------------------------

            records_extracted += len(data)

            # --------------------------------
            # RAW EVENT
            # --------------------------------

            load_raw_event(
                batch_id=batch_id,
                source="binance",
                symbol=symbol,
                interval="1m",
                payload=data,
                ingested_at=ingested_at
            )

            # --------------------------------
            # TRANSFORM + VALIDATE
            # --------------------------------

            clean, quarantined = process_klines(
                symbol=symbol,
                raw_klines=data,
                interval="1m",
                batch_id=batch_id,
                ingested_at=ingested_at
            )

            # --------------------------------
            # UPDATE COUNTERS
            # --------------------------------

            records_loaded += len(clean)
            records_quarantined += len(quarantined)

            # --------------------------------
            # LOAD CLEAN EVENTS
            # --------------------------------

            if clean:

                inserted = load_clean_events(
                    clean,
                    conn
                )

                logger.info(
                    f"{symbol} clean records | "
                    f"prepared={len(clean)} | "
                    f"inserted={inserted}"
                )

        # -----------------------------------
        # SUCCESS
        # -----------------------------------

        completed_at = datetime.now(timezone.utc)

        update_batch_status(
            batch_id=batch_id,
            status="SUCCESS",
            completed_at=completed_at,
            records_extracted=records_extracted,
            records_loaded=records_loaded,
            records_quarantined=records_quarantined
        )

        logger.info(
            f"Pipeline batch completed | "
            f"batch_id={batch_id} | "
            f"extracted={records_extracted} | "
            f"loaded={records_loaded} | "
            f"quarantined={records_quarantined}"
        )

        return batch_id

    except Exception as err:

        # -----------------------------------
        # FAILURE
        # -----------------------------------

        completed_at = datetime.now(timezone.utc)

        logger.exception(
            f"Pipeline batch failed | "
            f"batch_id={batch_id}"
        )

        update_batch_status(
            batch_id=batch_id,
            status="FAILED",
            completed_at=completed_at,
            records_extracted=records_extracted,
            records_loaded=records_loaded,
            records_quarantined=records_quarantined,
            error_message=str(err)
        )

        raise

    finally:

        # -----------------------------------
        # CLOSE DATABASE CONNECTION
        # -----------------------------------

        conn.close()

        logger.info(
            f"Database connection closed | "
            f"batch_id={batch_id}"
        )


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    run_pipeline()
