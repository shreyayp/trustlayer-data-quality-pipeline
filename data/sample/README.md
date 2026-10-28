# NYC 311-shaped synthetic sample

`nyc311_sample.csv` is **synthetic teaching data**, not a downloaded extract from NYC Open Data. Its columns are based on selected fields in the official NYC 311 dataset and it contains intentionally malformed records so the pipeline can run offline and tests stay deterministic. Do not present the sample's counts as real NYC statistics. To fetch current real records, use `src/trustlayer/download_nyc311.py` and cite the official source documented in `docs/03-data-source.md`.
