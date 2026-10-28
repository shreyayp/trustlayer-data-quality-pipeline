# 5. SQL Cookbook — NYC 311

Run these queries after executing the pipeline. The local database path is `data/processed/trustlayer.db`.

## Count accepted service requests
```sql
SELECT COUNT(*) AS accepted_request_count
FROM service_requests;
```

## Request count by complaint type
```sql
SELECT complaint_type, COUNT(*) AS request_count
FROM service_requests
GROUP BY complaint_type
ORDER BY request_count DESC;
```

## Request count by agency
```sql
SELECT agency, COUNT(*) AS request_count
FROM service_requests
GROUP BY agency
ORDER BY request_count DESC;
```

## Open requests by complaint type
```sql
SELECT complaint_type, COUNT(*) AS open_count
FROM service_requests
WHERE LOWER(status) = 'open'
GROUP BY complaint_type
ORDER BY open_count DESC;
```

Status values from the source can vary, so inspect distinct values before relying on a specific label:
```sql
SELECT DISTINCT status
FROM service_requests
ORDER BY status;
```

## Latest pipeline runs
```sql
SELECT run_id, status, input_rows, valid_rows, rejected_rows,
       duration_seconds, started_at
FROM pipeline_runs
ORDER BY run_id DESC;
```

## Most common rejection reasons
```sql
SELECT rejection_reason, COUNT(*) AS rejected_count
FROM rejected_records
GROUP BY rejection_reason
ORDER BY rejected_count DESC;
```

## Interview concepts
- `COUNT(*)` counts rows.
- `WHERE` filters rows before aggregation.
- `GROUP BY` aggregates records by a category.
- `ORDER BY ... DESC` sorts largest values first.
- A primary key protects the accepted table from duplicate request IDs.
