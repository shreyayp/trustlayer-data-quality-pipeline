import pandas as pd
from trustlayer.pipeline import run_pipeline
from trustlayer.database import connect

def test_pipeline_loads_valid_and_quarantines_invalid(tmp_path):
    input_path = tmp_path / "input.csv"
    db_path = tmp_path / "test.db"
    report_dir = tmp_path / "reports"
    pd.DataFrame([
        {"unique_key":"101","created_date":"2026-02-01T10:00:00","closed_date":"",
         "agency":"DOT","complaint_type":"Pothole","descriptor":"Road issue","incident_zip":"10001","status":"Open"},
        {"unique_key":"","created_date":"bad-date","closed_date":"",
         "agency":"DOT","complaint_type":"Pothole","descriptor":"Bad row","incident_zip":"10001","status":"Open"},
    ]).to_csv(input_path, index=False)
    result = run_pipeline(input_path, db_path, report_dir)
    assert result["status"] == "SUCCESS"
    assert result["input_rows"] == 2
    assert result["valid_rows"] == 1
    assert result["rejected_rows"] == 1
    with connect(db_path) as con:
        assert con.execute("SELECT COUNT(*) FROM service_requests").fetchone()[0] == 1
        assert con.execute("SELECT COUNT(*) FROM rejected_records").fetchone()[0] == 1
        assert con.execute("SELECT COUNT(*) FROM pipeline_runs").fetchone()[0] == 1
    assert (report_dir / "quality_report.json").exists()

def test_rerun_does_not_duplicate_valid_rows(tmp_path):
    input_path = tmp_path / "input.csv"
    db_path = tmp_path / "test.db"
    report_dir = tmp_path / "reports"
    pd.DataFrame([
        {"unique_key":"101","created_date":"2026-02-01T10:00:00","closed_date":"",
         "agency":"DOT","complaint_type":"Pothole","descriptor":"Road issue","incident_zip":"10001","status":"Open"},
    ]).to_csv(input_path, index=False)
    run_pipeline(input_path, db_path, report_dir)
    run_pipeline(input_path, db_path, report_dir)
    with connect(db_path) as con:
        assert con.execute("SELECT COUNT(*) FROM service_requests").fetchone()[0] == 1
        assert con.execute("SELECT COUNT(*) FROM pipeline_runs").fetchone()[0] == 2
