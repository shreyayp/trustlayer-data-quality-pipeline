"""Data quality rules for NYC 311-style NYC 311 service-request records."""
from __future__ import annotations
import pandas as pd

REQUIRED_COLUMNS = [
    "unique_key", "created_date", "agency", "complaint_type", "status"
]

def validate_records(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Return (valid_records, rejected_records).

    Rules:
    - Required columns must exist; otherwise raise ValueError.
    - unique_key must be present and unique (first occurrence is retained).
    - created_date must parse as a timestamp.
    - agency, complaint_type, and status must not be blank.
    - closed_date is optional; if present, it must parse when nonblank.
    Rejected rows include a rejection_reason field. This deliberately keeps
    rejected data for audit instead of silently deleting it.
    """
    missing = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    work = df.copy()
    reasons = [[] for _ in range(len(work))]
    work = work.reset_index(drop=True)

    for col in ["unique_key", "agency", "complaint_type", "status"]:
        blank = work[col].isna() | work[col].astype(str).str.strip().eq("")
        for i in work.index[blank]:
            reasons[i].append(f"{col}_missing")

    created = pd.to_datetime(work["created_date"], errors="coerce", utc=True)
    for i in work.index[created.isna()]:
        reasons[i].append("created_date_invalid")

    if "closed_date" in work.columns:
        raw_closed = work["closed_date"]
        has_value = raw_closed.notna() & raw_closed.astype(str).str.strip().ne("")
        closed = pd.to_datetime(raw_closed, errors="coerce", utc=True)
        for i in work.index[has_value & closed.isna()]:
            reasons[i].append("closed_date_invalid")
        for i in work.index[has_value & created.notna() & closed.notna() & (closed < created)]:
            reasons[i].append("closed_before_created")

    duplicate = work["unique_key"].notna() & work["unique_key"].astype(str).duplicated(keep="first")
    for i in work.index[duplicate]:
        reasons[i].append("duplicate_unique_key")

    work["rejection_reason"] = [";".join(r) for r in reasons]
    rejected = work[work["rejection_reason"].ne("")].copy()
    valid = work[work["rejection_reason"].eq("")].copy()
    valid = valid.drop(columns=["rejection_reason"])
    return valid.reset_index(drop=True), rejected.reset_index(drop=True)
