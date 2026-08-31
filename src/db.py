import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

if __name__ == "__main__":
    try:
        conn = get_db_connection()
        print("Neon PostgreSQL connection successful.")
        conn.close()
    except Exception as err:
        print(f"Database connection failed: {err}")

#def get_db_connection():
    #conn=psycopg2.connect(
        #host=DATABASE_HOST,
        #port=DATABASE_PORT,
        #dbname=DATABASE_NAME,
        #user=DATABASE_USER,
        #password=DATABASE_PASSWORD
    #)
    #return conn