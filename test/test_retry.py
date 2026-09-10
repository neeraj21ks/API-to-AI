from src.db import get_db_connection
from src.load import retry_batch


FAILED_BATCH_ID = "22002093-0e9e-4a9a-9275-49ea7e9df908"


def main():

    conn = get_db_connection()

    try:

        print("===== RETRY TEST =====")

        new_batch_id = retry_batch(
            conn,
            FAILED_BATCH_ID
        )

        print(f"Original batch: {FAILED_BATCH_ID}")
        print(f"Retry batch:    {new_batch_id}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()