"""Central project configuration."""
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
SAMPLE_DATA = ROOT_DIR / "data" / "sample" / "nyc311_sample.csv"
RAW_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
REPORT_DIR = ROOT_DIR / "reports" / "generated"
DEFAULT_DB = PROCESSED_DIR / "trustlayer.db"
