"""Download a small recent sample from the official NYC Open Data API.

The checked-in sample is synthetic and is provided for deterministic offline tests.
This optional script fetches current public records for an up-to-date real-data run.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import requests
import pandas as pd

API_URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"
FIELDS = ["unique_key", "created_date", "closed_date", "agency",
          "complaint_type", "descriptor", "incident_zip", "status"]

def download(output: str | Path, limit: int = 1000, since: str = "2025-01-01T00:00:00") -> int:
    if limit < 1 or limit > 50000:
        raise ValueError("limit must be between 1 and 50000")
    params = {
        "$select": ",".join(FIELDS),
        "$where": f"created_date >= '{since}'",
        "$order": "created_date DESC",
        "$limit": limit
    }
    response = requests.get(API_URL, params=params, timeout=60,
                            headers={"User-Agent": "TrustLayer-learning-project/1.0"})
    response.raise_for_status()
    payload = response.json()
    frame = pd.DataFrame(payload, columns=FIELDS)
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(target, index=False)
    return len(frame)

def main() -> None:
    parser = argparse.ArgumentParser(description="Download recent NYC 311 service requests.")
    parser.add_argument("--output", default="data/raw/nyc311_recent.csv")
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--since", default="2025-01-01T00:00:00")
    args = parser.parse_args()
    count = download(args.output, args.limit, args.since)
    print(f"Downloaded {count} rows to {args.output}")

if __name__ == "__main__":
    main()
