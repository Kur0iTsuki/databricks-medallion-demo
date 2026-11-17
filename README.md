# Databricks Medallion Demo

A dependency-free Medallion Lakehouse demonstration using Kaggle's real-world **Online Retail** dataset. It is designed for portfolio discussion only and contains no employer data or implementation details.

## Flow

```text
Kaggle Online Retail CSV -> Bronze (raw input) -> Silver (validated + de-duplicated) -> Gold (daily aggregates)
```

- **Bronze:** Kaggle Online Retail purchase-line events.
- **Silver:** cancelled invoices and invalid values are excluded; valid records are normalized to a line-level schema.
- **Gold:** daily transaction-line counts and integer-cent totals are aggregated by currency.

## Run the real-data pipeline

Requires Python 3.11+, `curl`, and `unzip`; no Python packages need to be installed.

The raw CSV is intentionally not committed. The download helper retrieves the public source into the ignored `data/raw/` directory, keeping the repository lightweight and reproducible.

```bash
sh scripts/download_kaggle_dataset.sh
python3 run_kaggle_pipeline.py
```

The command prints the number of valid purchase lines, the number of daily Gold aggregates, and a small preview. To use a CSV stored elsewhere, pass its path explicitly:

```bash
python3 run_kaggle_pipeline.py /path/to/Online_Retail.csv
```

## Verify

```bash
python3 -m unittest discover -s tests -v
```

## Optional synthetic quick demo

For a fast, offline illustration of the same Silver and Gold logic, run:

```bash
python3 run_pipeline.py
```

The source is [Online Retail on Kaggle](https://www.kaggle.com/datasets/tunguz/online-retail), published under **CC0: Public Domain**. It contains anonymized transaction-level data from a UK-based online retailer. The pipeline treats unit prices as GBP and excludes cancelled invoices and non-positive quantities or prices.

## Design choices

- Monetary values use integer cents to avoid floating-point rounding.
- The first valid occurrence of a transaction ID is retained as the deterministic de-duplication rule.
- The code mirrors Lakehouse concepts without requiring a Databricks workspace.
- The download and transformation flow is designed to be reproducible with a publicly available, permissively licensed source.
