import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://shopworthy:shopworthy123@postgres:5432/inventory")


def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def query(sql, params=None):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        results = cur.fetchall()
        conn.close()
        return [dict(r) for r in results]
    except Exception as e:
        conn.close()
        raise e


def execute(sql, params=None):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        conn.close()
    except Exception as e:
        conn.rollback()
        conn.close()
        raise e
