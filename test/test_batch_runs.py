from src.db import get_db_connection
from src.load import (
    create_batch_run,
    update_batch_success,
    update_batch_failure,
)


def main():

    conn = get_db_connection()

    try:

        # -------------------------------
        # Create batch
        # -------------------------------

        batch_id = create_batch_run(conn)

        print(f"Created batch: {batch_id}")

        # -------------------------------
        # Mark successful
        # -------------------------------

        update_batch_success(
            conn,
            batch_id,
            records_extracted=30,
            records_loaded=30,
            records_quarantined=0,
        )

        print("Batch marked SUCCESS")

    finally:
        conn.close()


if __name__ == "__main__":
    main()