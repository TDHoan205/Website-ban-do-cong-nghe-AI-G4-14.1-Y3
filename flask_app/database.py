"""
Database configuration – SQLAlchemy + pyodbc for SQL Server.
Uses Windows Authentication (Trusted_Connection=yes).
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool

# ── SQL Server connection ────────────────────────────────────────────────
SQL_SERVER = os.getenv("SQL_SERVER", "DESKTOP-1TM8FSO")
DATABASE_NAME = os.getenv("DATABASE_NAME", "TechShopWebsite2")

# Windows Authentication via pyodbc
CONNECTION_STRING = (
    f"mssql+pyodbc://{SQL_SERVER}/{DATABASE_NAME}"
    f"?driver=ODBC+Driver+17+for+SQL+Server"
    f"&Trusted_Connection=yes"
    f"&Encrypt=yes"
    f"&TrustServerCertificate=yes"
    f"&charset=utf8"
    f"&unicode_results=true"
)

# ── SQLAlchemy Engine ───────────────────────────────────────────────────
engine = create_engine(
    CONNECTION_STRING,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,
    connect_args={
        "unicode_results": True,
        "ansi": False,
    },
)

# ── Session factory ─────────────────────────────────────────────────────
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ── Base class for models ──────────────────────────────────────────────
Base = declarative_base()

# ── Dependency: get_db() for FastAPI endpoints ─────────────────────────
def get_db():
    """Yields a database session; ensures it's closed after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ── Health check ────────────────────────────────────────────────────────
def check_connection() -> bool:
    """Returns True if we can reach the database."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"[DB] Connection failed: {e}")
        return False
