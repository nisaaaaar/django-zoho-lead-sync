import time
import psycopg2
from psycopg2 import OperationalError
import os

DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_PORT = 5432

print("Waiting for PostgreSQL...")

while True:
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
        )
        conn.close()
        print("PostgreSQL is ready!")
        break
    except OperationalError:
        print("PostgreSQL unavailable, waiting 1s...")
        time.sleep(1)
