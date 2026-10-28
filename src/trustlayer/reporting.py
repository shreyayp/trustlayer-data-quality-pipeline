"""SQL summary and machine-readable quality report generation."""
from __future__ import annotations
import json
from pathlib import Path
import sqlite3
import pandas as pd

def build_report(con: sqlite3.Connection, output_dir: str | Path) -> dict:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    total = con.execute("SELECT COUNT(*) FROM service_requests").fetchone()[0]
    rejected = con.execute("SELECT COUNT(*) FROM rejected_records").fetchone()[0]
    latest = con.execute("""
        SELECT run_id, started_at, finished_at, status, input_rows, valid_rows,
               rejected_rows, inserted_rows, duration_seconds, error_message
        FROM pipeline_runs ORDER BY run_id DESC LIMIT 1
    """).fetchone()
    by_type = pd.read_sql_query("""
        SELECT complaint_type, COUNT(*) AS request_count
        FROM service_requests
        GROUP BY complaint_type ORDER BY request_count DESC
    """, con)
    by_type.to_csv(out / "requests_by_problem.csv", index=False)
    reasons = pd.read_sql_query("""
        SELECT rejection_reason, COUNT(*) AS rejected_count
        FROM rejected_records
        GROUP BY rejection_reason ORDER BY rejected_count DESC
    """, con)
    reasons.to_csv(out / "rejection_summary.csv", index=False)
    report = {
        "project": "TrustLayer",
        "description": "Data quality and pipeline observability demonstration",
        "valid_records_in_database": total,
        "rejected_record_events": rejected,
        "latest_run": dict(zip(
            ["run_id", "started_at", "finished_at", "status", "input_rows",
             "valid_rows", "rejected_rows", "inserted_rows", "duration_seconds",
             "error_message"], latest
        )) if latest else None,
        "note": "Counts reflect this local database and all run history; reruns may add rejection events."
    }
    (out / "quality_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
