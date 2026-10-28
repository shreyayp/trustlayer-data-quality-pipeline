# 9. Interview Preparation

## 60-second project explanation
"TrustLayer is a Python and SQL data quality pipeline built around NYC 311 service-request data. It can read a local CSV or a limited extract from the NYC Open Data API, validate request IDs and timestamps, separate valid and invalid records, load accepted rows into SQLite, and retain rejected rows with reasons. It records pipeline run metrics and produces SQL summary reports. I wrote pytest unit and integration tests and configured GitHub Actions to run them on pushes and pull requests."

## Common questions

### What is ETL?
Extracting data from a source, transforming it into a consistent structure, and loading it into a target such as a database.

### Why NYC 311 data?
It is a public, real-world operational dataset with dates, categories, agencies, statuses, and identifiers. It provides realistic examples for data validation and SQL aggregation. The bundled sample is synthetic for repeatability; the downloader accesses the real source.

### Why SQLite?
It is easy to run locally and demonstrates relational tables, primary keys, SQL queries, and data loading without needing a separate server.

### Why quarantine rejected rows?
It preserves the original values and reasons for investigation rather than silently dropping problematic records.

### What is idempotency?
Rerunning the same input should not duplicate accepted rows. TrustLayer uses a primary key and upsert logic for this purpose.

### What does GitHub Actions do?
It automatically executes the configured tests when code is pushed or a pull request is opened, making regressions visible.

### Unit test vs integration test?
A unit test checks one function/rule. An integration test checks components working together, such as validation, SQLite persistence, and report generation.

### What are limitations?
This is a portfolio-scale project, not a production service. It has no scheduler or alerting service. The initial freshness monitoring records run timestamps but does not enforce a configurable source freshness SLA.

## Honest portfolio practice
Be ready to explain every module and demonstrate a rejected record. Do not claim production scale, real-time streaming, or production deployment.
