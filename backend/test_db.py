# test_db_conn.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise SystemExit("No DATABASE_URL in env")

# Try require SSL (work with Supabase/remote PG servers)
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"},
    pool_pre_ping=True,   # helps with stale connections / EOF
    echo=False
)

try:
    with engine.connect() as conn:
        print("Connected, SELECT 1 ->", conn.execute(text("SELECT 1")).scalar())
except Exception as e:
    print("Connection test failed:", repr(e))
