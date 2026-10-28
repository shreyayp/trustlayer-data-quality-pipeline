# 1. Project Overview — TrustLayer

## Problem
NYC 311 service-request data is public and useful for learning analytics, but records can have missing identifiers, duplicate keys, invalid timestamps, blank categories, or contradictory dates. Poor-quality rows can produce misleading downstream reports.

## Solution
TrustLayer downloads a limited recent sample from the official NYC Open Data API (optional), validates CSV records, stores accepted rows in SQLite, quarantines rejected rows with reasons, records pipeline-run metrics, and generates reports. The bundled synthetic data makes development reproducible without network access.

## Goals
- Work with one consistent domain: NYC 311 service requests.
- Demonstrate extract, transform, and load (ETL).
- Make data-quality rules explicit and testable.
- Preserve rejected rows for audit and investigation.
- Demonstrate SQL fundamentals and SQLite schema design.
- Automate tests with pytest and GitHub Actions.

## Success criteria
- A fresh setup can install dependencies and run the pipeline.
- Invalid records are rejected with clear reasons.
- Valid records are stored in SQLite.
- Re-running the same input does not duplicate accepted rows.
- Tests pass locally and in GitHub Actions.

## Out of scope
This is not a production monitoring service. It does not guarantee that the source's information is factually correct, and it does not include a scheduler, production alerting, or a live dashboard.
