# 2. Beginner Concepts

## NYC 311 service request
A service request is a record submitted to a city service system. The dataset contains fields such as request ID, creation/closure dates, agency, complaint type, and status.

## Dataset, record, field
A dataset is a collection of related records. A record is one row; a field is one column.

## ETL
- **Extract:** read a CSV or download data from the NYC Open Data API.
- **Transform:** normalize/validate fields and classify rows as valid or rejected.
- **Load:** save accepted and rejected records to SQLite.

## Data quality dimensions
- **Completeness:** required fields are populated.
- **Uniqueness:** each `unique_key` identifies at most one accepted record.
- **Validity:** timestamps parse correctly and required values are nonblank.
- **Consistency:** a close date should not be earlier than the creation date.
- **Freshness:** data is recent enough for the analysis. This initial version tracks run timestamps; a future version could enforce a configurable source-data freshness threshold.

## SQL and SQLite
SQL is the language used to query relational data. SQLite is a lightweight relational database stored in a local file. Python includes SQLite support through `sqlite3`, so no separate database server is needed.

## Primary key
A primary key uniquely identifies a row. TrustLayer uses `unique_key` as the accepted-record table's primary key.

## Quarantine
Rejected records are saved with one or more reasons. Keeping them supports investigation instead of silently discarding data.

## Idempotency
Reprocessing the same input should not create duplicate accepted rows. TrustLayer uses a primary key and upsert logic to update the row associated with an existing request key.

## Logging and observability
Logs describe program activity. Run metrics describe input count, valid/rejected counts, status, duration, and errors.

## Unit tests, integration tests, and CI
Unit tests check individual validation rules. Integration tests check the whole pipeline with a temporary CSV and database. GitHub Actions runs the test suite on pushes and pull requests so failures are visible early.
