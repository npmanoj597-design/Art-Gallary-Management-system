import os
from sqlalchemy import text
from dotenv import load_dotenv

# Load repo .env (same as backend main.py)
_SCRIPT_DIR = os.path.dirname(__file__)
_REPO_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, ".."))
_ENV_PATH = os.path.join(_REPO_ROOT, ".env")
load_dotenv(dotenv_path=_ENV_PATH, override=False)

from app.db import engine

files = [
    os.path.join(_REPO_ROOT, "sql", "procedures", "GetArtistRevenue.sql"),
    os.path.join(_REPO_ROOT, "sql", "procedures", "BookTicket.sql"),
]

with engine.begin() as conn:
    for f in files:
        print("Applying", f)
        # Defensive: drop existing procedures with known legacy signatures
        if f.lower().endswith("getartistrevenue.sql"):
            try:
                conn.execute(text("DROP PROCEDURE IF EXISTS GetArtistRevenue(integer, numeric);"))
            except Exception:
                pass
            try:
                conn.execute(text("DROP FUNCTION IF EXISTS getartistrevenue(integer);"))
            except Exception:
                pass
        if f.lower().endswith("bookticket.sql"):
            try:
                conn.execute(text("DROP PROCEDURE IF EXISTS BookTicket(integer, integer, varchar, integer);"))
            except Exception:
                pass
            try:
                conn.execute(text("DROP FUNCTION IF EXISTS bookticket(integer, integer, varchar);"))
            except Exception:
                pass

        sql = open(f, "r", encoding="utf-8").read()
        conn.execute(text(sql))
print("Done")
