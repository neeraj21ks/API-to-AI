import os
import psycopg
from dotenv import load_dotenv
from psycopg.types.json import Jsonb

load_dotenv()
database_url = os.getenv("DATABASE_URL")

#createing SQL table
create_table_sql = """
CREATE TABLE IF NOT EXISTS clean_klines (
    symbol VARCHAR(20) NOT NULL,
    open_time TIMESTAMPTZ NOT NULL,
    close_time TIMESTAMPTZ NOT NULL,
    open NUMERIC NOT NULL,
    high NUMERIC NOT NULL,
    low NUMERIC NOT NULL,
    close NUMERIC NOT NULL,
    volume NUMERIC NOT NULL,
    PRIMARY KEY (symbol, open_time)
)
"""

def load_raw_event(
    batch_id,
    source,
    symbol,
    interval,
    payload,
    ingested_at
):
    insert_sql = """
        INSERT INTO raw_events (
            batch_id,
            source,
            symbol,
            interval,
            payload,
            ingested_at
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                insert_sql,
                (
                    batch_id,
                    source,
                    symbol,
                    interval,
                    Jsonb(payload),
                    ingested_at
                )
            )

        conn.commit()

#data loading to Neon
def load_to_neon(clean):
    #coonecting with Neon
    try:
        with psycopg.connect(database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(create_table_sql)  #create
                load_clean_klines(clean, cur)   #load
            conn.commit()  # Commit if all is well
            print("Data load completed successfully.")
    except Exception as e:
        #conn.rollback()  # Rollback if something goes wrong
        print(f"Error during database operation: {e}")  # Log the error
    #finally:
      #  pass  # Ensure the connection is closed

def load_clean_klines(clean,cur):
    for record in clean:
        insert_sql="""Insert into clean_klines(
        symbol,open_time,close_time,open,high,low,close,volume)
        values (%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (symbol, open_time) DO NOTHING"""
        columns= ["symbol","open_time","close_time","open","high","low","close","volume"]
        values =tuple(record[col] for col in columns)
        cur.execute(insert_sql,values) 

def load_clean_events(clean):
    try:
        with psycopg.connect(database_url) as conn:
            with conn.cursor() as cur:

                insert_sql = """
                    INSERT INTO clean_events (
                        symbol,
                        interval,
                        open_time,
                        close_time,
                        open,
                        high,
                        low,
                        close,
                        volume,
                        source,
                        batch_id,
                        ingested_at
                    )
                    VALUES (
                        %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (
                        symbol,
                        interval,
                        open_time
                    )
                    DO NOTHING
                """

                for record in clean:
                    values = (
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
                        record["ingested_at"]
                    )

                    cur.execute(insert_sql, values)

            conn.commit()

        print("Clean events loaded successfully.")

    except Exception as e:
        print(f"Error loading clean events: {e}")

def create_batch(batch_id, source, started_at):
    insert_sql = """
        INSERT INTO pipeline_batches (
            batch_id,
            source,
            started_at,
            status
        )
        VALUES (%s, %s, %s, %s)
    """

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                insert_sql,
                (
                    batch_id,
                    source,
                    started_at,
                    "RUNNING"
                )
            )

        conn.commit()


def update_batch_status(
    batch_id,
    status,
    completed_at=None,
    records_extracted=0,
    records_loaded=0,
    records_quarantined=0,
    error_message=None
):
    update_sql = """
        UPDATE pipeline_batches
        SET
            status = %s,
            completed_at = %s,
            records_extracted = %s,
            records_loaded = %s,
            records_quarantined = %s,
            error_message = %s
        WHERE batch_id = %s
    """

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                update_sql,
                (
                    status,
                    completed_at,
                    records_extracted,
                    records_loaded,
                    records_quarantined,
                    error_message,
                    batch_id
                )
            )

        conn.commit()