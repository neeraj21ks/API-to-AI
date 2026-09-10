from src.db import get_db_connection
from src.load import (
    create_batch_run,
    update_batch_failure,
)


def main():

    conn = get_db_connection()

    try:
        batch_id = create_batch_run(conn)

        print(f"Created batch: {batch_id}")

        # Simulate pipeline failure
        error_message = "Simulated pipeline failure for testing"

        update_batch_failure(
            conn,
            batch_id,
            error_message,
        )

        print("Batch marked FAILED")

    finally:
        conn.close()


if __name__ == "__main__":
    main()