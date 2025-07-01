import psycopg2
from contextlib import contextmanager

DB_NAME = 'postgres'
DB_USER = 'mohamed'
DB_PASSWORD = 'Mohamed55555'
DB_HOST = 'localhost'

@contextmanager
def get_connection():
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
        )
        print("Database connection successful")
        cur = conn.cursor()
        yield conn, cur
    except psycopg2.Error as error:
        print(f"Database connection failed: {error}")
        raise
    finally:
        if cur: 
            cur.close()
        if conn:
            conn.close()
