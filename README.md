# Databricks Medallion Demo

A dependency-free, synthetic demonstration of a Medallion Lakehouse flow. It is designed for portfolio discussion only and contains no proprietary code, customer data, or employer implementation details.

## Flow

```text
Synthetic JSON events -> Bronze (raw input) -> Silver (validated + de-duplicated) -> Gold (daily aggregates)
```

- **Bronze:** incoming synthetic transaction events.
- **Silver:** required fields are validated and duplicate transaction IDs are removed.
- **Gold:** daily transaction counts and integer-cent totals are aggregated by currency.

## Run

Requires Python 3.11+ and no third-party packages.

```bash
python3 run_pipeline.py
python3 -m unittest discover -s tests -v
```

## Design choices

- Monetary values use integer cents to avoid floating-point rounding.
- The first valid occurrence of a transaction ID is retained as the deterministic de-duplication rule.
- The code mirrors Lakehouse concepts without requiring a Databricks workspace.
