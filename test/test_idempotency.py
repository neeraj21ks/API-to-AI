import os
from datetime import timedelta

from dotenv import load_dotenv
import psycopg

from src.load import load_clean_events
from src.transform import transform_kline


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

BATCH_ID = "3dfb6a2c-2b07-43aa-8f7f-bfa0d71f56ff"


def main():

    with psycopg.connect(DATABASE_URL) as conn:

        # -----------------------------------------
        # 1. Read existing raw events
        # -----------------------------------------
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    symbol,
                    interval,
                    payload,
                    batch_id,
                    ingested_at
                FROM raw_events
                WHERE batch_id = %s
                ORDER BY symbol
                """,
                (BATCH_ID,)
            )

            raw_events = cur.fetchall()

        print(f"Raw API events found: {len(raw_events)}")

        # -----------------------------------------
        # 2. Transform existing raw payloads
        # -----------------------------------------
        clean_records = []

        for symbol, interval, payload, batch_id, ingested_at in raw_events:

            for raw_kline in payload:

                record = transform_kline(
                    symbol=symbol,
                    interval=interval,
                    kline=raw_kline,
                    batch_id=batch_id,
                    ingested_at=ingested_at
                )

                clean_records.append(record)

        print(f"Clean records prepared: {len(clean_records)}")

        # -----------------------------------------
        # 3. Replay entire batch
        # -----------------------------------------
        inserted_count, duplicate_count = load_clean_events(
            clean_records,
            conn
        )

        print()
        print("===== FULL REPLAY TEST =====")
        print(f"Inserted:   {inserted_count}")
        print(f"Duplicate:  {duplicate_count}")
        print(f"Total:      {inserted_count + duplicate_count}")

        # -----------------------------------------
        # 4. Mixed duplicate + new test
        # -----------------------------------------

        existing_records = clean_records[:3]

        new_records = []

        for record in clean_records[:2]:

            new_record = record.copy()

            new_record["open_time"] = (
                new_record["open_time"] + timedelta(hours=1)
            )

            new_record["close_time"] = (
                new_record["close_time"] + timedelta(hours=1)
            )

            new_records.append(new_record)

        mixed_records = existing_records + new_records

        print()
        print("===== MIXED IDEMPOTENCY TEST =====")

        inserted_count, duplicate_count = load_clean_events(
            mixed_records,
            conn
        )

        print(f"Inserted:   {inserted_count}")
        print(f"Duplicate:  {duplicate_count}")
        print(f"Total:      {inserted_count + duplicate_count}")


if __name__ == "__main__":
    main()

