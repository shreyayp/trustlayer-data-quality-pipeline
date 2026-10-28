# 3. Data Source — NYC 311 Service Requests

## Official dataset
**NYC Open Data — 311 Service Requests from 2020 to Present**

- Dataset page: https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9
- API documentation: https://dev.socrata.com/foundry/data.cityofnewyork.us/erm2-nwe9
- Data.gov catalog: https://catalog.data.gov/dataset/311-service-requests-from-2010-to-present
- Publisher: NYC Open Data / NYC 311
- Access method: Socrata Open Data API (SODA)
- Update frequency: the dataset page describes daily updates.
- Accessed/design checked: 2026-10-29.

The dataset contains service-request information including unique request key, creation/closure dates, agency, complaint type, descriptor, location fields, and status. The full dataset is large and changes over time, so TrustLayer downloads a limited sample.

## Download recent records
From the project root:

```bash
python -m src.trustlayer.download_nyc311 --limit 1000 --since "2025-01-01T00:00:00"
```

The downloader writes `data/raw/nyc311_recent.csv`. The request filters for recent creation timestamps and sorts newest first. A network connection is required. The API may return fewer than the requested number of rows depending on data availability.

Then run:

```bash
PYTHONPATH=src python -m trustlayer.pipeline --input data/raw/nyc311_recent.csv
```

## API fields used
- `unique_key`: request identifier; required and unique.
- `created_date`: request creation timestamp; required and parseable.
- `closed_date`: optional closure timestamp; if present, it must parse and must not precede creation.
- `agency`: responsible agency; required and nonblank.
- `complaint_type`: request/problem category; required and nonblank.
- `descriptor`: optional descriptive detail.
- `incident_zip`: optional ZIP code retained as text.
- `status`: current request status; required and nonblank.

API field names are used in code; these may differ from display labels on the dataset website.

## Synthetic sample disclosure
`data/sample/nyc311_sample.csv` is synthetic teaching data shaped like selected NYC 311 fields. It contains deliberate errors for offline tests. It is not an official NYC download and its counts must not be described as real NYC statistics.

## Attribution and responsible use
When using downloaded records in a report or portfolio post, cite NYC Open Data, record the download date and query, and avoid committing large raw extracts. Follow the dataset and API terms. Do not enrich public records with personal data from unrelated sources.
