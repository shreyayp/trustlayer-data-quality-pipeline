# 4. Data Dictionary

| Field | Meaning | Required? | Validation |
|---|---|---:|---|
| `unique_key` | Unique NYC 311 request identifier | Yes | Nonblank and unique |
| `created_date` | Request creation timestamp | Yes | Must parse as datetime |
| `closed_date` | Request closure timestamp | No | If nonblank, must parse and not precede creation |
| `agency` | Responsible agency | Yes | Nonblank |
| `complaint_type` | Type/category of service request | Yes | Nonblank |
| `descriptor` | Additional detail | No | May be blank |
| `incident_zip` | ZIP code associated with request | No | Kept as text |
| `status` | Request status | Yes | Nonblank |

## Validation behavior
Rows failing one or more row-level rules are placed in `rejected_records` and receive semicolon-separated reasons. The first occurrence of a repeated request key is retained as eligible; later duplicate occurrences are rejected.

The sample file contains synthetic examples. Use the optional downloader for current real data.
