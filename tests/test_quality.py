import pandas as pd
import pytest
from trustlayer.quality import validate_records

def sample():
    return pd.DataFrame([
        {"unique_key":"1","created_date":"2026-01-02T10:00:00","closed_date":"2026-01-03T10:00:00",
         "agency":"NYPD","complaint_type":"Noise","descriptor":"Loud music","incident_zip":"10001","status":"Closed"},
        {"unique_key":"2","created_date":"2026-01-02T11:00:00","closed_date":"",
         "agency":"DSNY","complaint_type":"Missed Collection","descriptor":"Trash","incident_zip":"10002","status":"Open"},
    ])

def test_valid_records_pass():
    valid, rejected = validate_records(sample())
    assert len(valid) == 2
    assert len(rejected) == 0

def test_missing_required_value_is_rejected():
    df = sample()
    df.loc[0, "agency"] = ""
    valid, rejected = validate_records(df)
    assert len(valid) == 1
    assert "agency_missing" in rejected.iloc[0]["rejection_reason"]

def test_duplicate_key_is_rejected():
    df = sample()
    df.loc[1, "unique_key"] = "1"
    valid, rejected = validate_records(df)
    assert len(valid) == 1
    assert "duplicate_unique_key" in rejected.iloc[0]["rejection_reason"]

def test_invalid_created_date_is_rejected():
    df = sample()
    df.loc[0, "created_date"] = "not-a-date"
    _, rejected = validate_records(df)
    assert "created_date_invalid" in rejected.iloc[0]["rejection_reason"]

def test_closed_before_created_is_rejected():
    df = sample()
    df.loc[0, "closed_date"] = "2026-01-01T00:00:00"
    _, rejected = validate_records(df)
    assert "closed_before_created" not in rejected.iloc[0]["rejection_reason"]

def test_missing_required_column_raises():
    df = sample().drop(columns=["agency"])
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_records(df)
