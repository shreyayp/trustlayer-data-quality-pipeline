"""SQLite persistence and pipeline run history."""
from __future__ import annotations
import sqlite3
from pathlib import Path
import pandas as pd

def connect(db_path: str | Path) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.execute("PRAGMA foreign_keys = ON")
    return con

def initialize_database(con: sqlite3.Connection) -> None:
    con.executescript("""
    CREATE TABLE IF NOT EXISTS service_requests (
        unique_key TEXT PRIMARY KEY,
        created_date TEXT NOT NULL,
        closed_date TEXT,
        agency TEXT NOT NULL,
        complaint_type TEXT NOT NULL,
        descriptor TEXT,
        incident_zip TEXT,
        status TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS rejected_records (
        rejection_id INTEGER PRIMARY KEY AUTOINCREMENT,
        unique_key TEXT,
        created_date TEXT,
        closed_date TEXT,
        agency TEXT,
        complaint_type TEXT,
        descriptor TEXT,
        incident_zip TEXT,
        status TEXT,
        rejection_reason TEXT NOT NULL,
        rejected_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS pipeline_runs (
        run_id INTEGER PRIMARY KEY AUTOINCREMENT,
        started_at TEXT NOT NULL,
        finished_at TEXT NOT NULL,
        status TEXT NOT NULL,
        input_rows INTEGER NOT NULL,
        valid_rows INTEGER NOT NULL,
        rejected_rows INTEGER NOT NULL,
        inserted_rows INTEGER NOT NULL,
        duration_seconds REAL NOT NULL,
        error_message TEXT
    );
    """)
    con.commit()

def load_valid_records(con: sqlite3.Connection, df: pd.DataFrame) -> int:
    """Idempotent upsert: reruns update the same key rather than duplicate it."""
    if df.empty:
        return 0
    cols = ["unique_key", "created_date", "closed_date", "agency",
            "complaint_type", "descriptor", "incident_zip", "status"]
    frame = df.copy()
    for col in cols:
        if col not in frame.columns:
            frame[col] = None
    frame = frame[cols].copy()
    for col in ["created_date", "closed_date"]:
        frame[col] = frame[col].where(frame[col].notna(), None)
        frame[col] = frame[col].apply(lambda x: x.isoformat() if hasattr(x, "isoformat") else x)
    before = con.total_changes
    con.executemany("""
        INSERT INTO service_requests
        (unique_key, created_date, closed_date, agency, complaint_type,
         descriptor, incident_zip, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(unique_key) DO UPDATE SET
          created_date=excluded.created_date, closed_date=excluded.closed_date,
          agency=excluded.agency, complaint_type=excluded.complaint_type,
          descriptor=excluded.descriptor, incident_zip=excluded.incident_zip,
          status=excluded.status
    """, [tuple(None if pd.isna(v) else v for v in row) for row in frame.itertuples(index=False, name=None)])
    con.commit()
    return con.total_changes - before

def save_rejected_records(con: sqlite3.Connection, df: pd.DataFrame) -> int:
    if df.empty:
        return 0
    cols = ["unique_key", "created_date", "closed_date", "agency",
            "complaint_type", "descriptor", "incident_zip", "status", "rejection_reason"]
    frame = df.copy()
    for col in cols:
        if col not in frame.columns:
            frame[col] = None
    frame = frame[cols]
    con.executemany("""
        INSERT INTO rejected_records
        (unique_key, created_date, closed_date, agency, complaint_type,
         descriptor, incident_zip, status, rejection_reason)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [tuple(None if pd.isna(v) else v for v in row) for row in frame.itertuples(index=False, name=None)])
    con.commit()
    return len(frame)

def save_run(con: sqlite3.Connection, run: dict) -> None:
    con.execute("""
        INSERT INTO pipeline_runs
        (started_at, finished_at, status, input_rows, valid_rows, rejected_rows,
         inserted_rows, duration_seconds, error_message)
        VALUES (:started_at, :finished_at, :status, :input_rows, :valid_rows,
         :rejected_rows, :inserted_rows, :duration_seconds, :error_message)
    """, run)
    con.commit()
