"""Orchestrate ingestion, validation, SQLite loading, metrics, and reports."""
from __future__ import annotations
import argparse
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
from .config import SAMPLE_DATA, DEFAULT_DB, REPORT_DIR
from .database import connect, initialize_database, load_valid_records, save_rejected_records, save_run
from .quality import validate_records
from .reporting import build_report

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("trustlayer")

def run_pipeline(input_path: str | Path = SAMPLE_DATA,
                 db_path: str | Path = DEFAULT_DB,
                 report_dir: str | Path = REPORT_DIR) -> dict:
    started = datetime.now(timezone.utc)
    tick = time.perf_counter()
    input_rows = valid_rows = rejected_rows = inserted_rows = 0
    status, error_message = "SUCCESS", None
    try:
        logger.info("Reading input file: %s", input_path)
        raw = pd.read_csv(input_path, dtype=str, keep_default_na=True)
        input_rows = len(raw)
        valid, rejected = validate_records(raw)
        valid_rows, rejected_rows = len(valid), len(rejected)
        with connect(db_path) as con:
            initialize_database(con)
            inserted_rows = load_valid_records(con, valid)
            save_rejected_records(con, rejected)
            finished = datetime.now(timezone.utc)
            save_run(con, {
                "started_at": started.isoformat(),
                "finished_at": finished.isoformat(),
                "status": status,
                "input_rows": input_rows,
                "valid_rows": valid_rows,
                "rejected_rows": rejected_rows,
                "inserted_rows": inserted_rows,
                "duration_seconds": round(time.perf_counter() - tick, 4),
                "error_message": error_message
            })
            build_report(con, report_dir)
        logger.info("Completed: input=%s valid=%s rejected=%s db_changes=%s",
                    input_rows, valid_rows, rejected_rows, inserted_rows)
        return {"status": status, "input_rows": input_rows, "valid_rows": valid_rows,
                "rejected_rows": rejected_rows, "inserted_rows": inserted_rows}
    except Exception as exc:
        status, error_message = "FAILED", str(exc)
        logger.exception("Pipeline failed")
        # Record a failure if the database itself is available.
        try:
            with connect(db_path) as con:
                initialize_database(con)
                save_run(con, {
                    "started_at": started.isoformat(),
                    "finished_at": datetime.now(timezone.utc).isoformat(),
                    "status": status, "input_rows": input_rows,
                    "valid_rows": valid_rows, "rejected_rows": rejected_rows,
                    "inserted_rows": inserted_rows,
                    "duration_seconds": round(time.perf_counter() - tick, 4),
                    "error_message": error_message
                })
        except Exception:
            logger.exception("Could not record failed run")
        raise

def main() -> None:
    parser = argparse.ArgumentParser(description="Run TrustLayer data quality pipeline.")
    parser.add_argument("--input", default=str(SAMPLE_DATA), help="Input CSV path")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="SQLite database path")
    parser.add_argument("--reports", default=str(REPORT_DIR), help="Report output directory")
    args = parser.parse_args()
    result = run_pipeline(args.input, args.db, args.reports)
    print("\nTrustLayer run summary")
    for key, value in result.items():
        print(f"{key.replace('_', ' ').title()}: {value}")

if __name__ == "__main__":
    main()
