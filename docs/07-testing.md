# 7. Testing Strategy

## Run tests
```bash
PYTHONPATH=src pytest -v
```

## Test coverage in this starter project
- Required values are checked.
- Duplicate request keys are rejected.
- Invalid creation timestamps are rejected.
- Closure before creation is rejected.
- Missing required columns raise a clear error.
- An integration test verifies valid rows are loaded and invalid rows quarantined.
- An idempotency test runs the same input twice and checks accepted rows are not duplicated.

## Test a failure manually
Change a test input's `created_date` to `not-a-date`. The validator should reject it with `created_date_invalid`.

## What tests do not prove
Tests cover the rules written by the developer. Passing tests do not prove every possible data problem is covered. New source fields and business requirements should lead to new tests.
