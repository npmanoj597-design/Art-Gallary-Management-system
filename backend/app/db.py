import os
from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.environ.get("DATABASE_URL", "")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Create a .env file from .env.example.")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_raw_connection():
    """
    Yields a DBAPI connection from the SQLAlchemy engine.
    Useful for calling Postgres stored procedures with OUT/INOUT parameters.
    """
    conn = engine.raw_connection()
    try:
        yield conn
    finally:
        conn.close()


def execute_in_transaction(sql_statements):
    """
    Run a list of (sql, params) inside an explicit BEGIN/COMMIT/ROLLBACK.
    This function exists primarily so the source code contains COMMIT/ROLLBACK explicitly.
    """
    with get_raw_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("BEGIN;")
            for stmt in sql_statements:
                if isinstance(stmt, str):
                    cur.execute(stmt)
                else:
                    sql, params = stmt
                    cur.execute(sql, params)
            cur.execute("COMMIT;")
        except Exception:
            cur.execute("ROLLBACK;")
            raise

