"""A dependency-free, synthetic Medallion pipeline example."""

import csv
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


REQUIRED_FIELDS = ("transaction_id", "event_timestamp", "amount_cents", "currency")


def load_online_retail_csv(path: Path) -> list[dict]:
    """Normalize Kaggle's Online Retail CSV into valid, purchase-only line records."""
    records = []
    # Kaggle's file includes Latin-1 product descriptions such as the pound symbol.
    with path.open(newline="", encoding="latin-1") as source:
        for line_number, row in enumerate(csv.DictReader(source), start=1):
            invoice = row["InvoiceNo"].strip()
            quantity = int(row["Quantity"])
            unit_price = Decimal(row["UnitPrice"])
            if invoice.startswith("C") or quantity <= 0 or unit_price <= 0:
                continue

            timestamp = datetime.strptime(row["InvoiceDate"], "%m/%d/%y %H:%M").replace(tzinfo=timezone.utc)
            amount_cents = int((Decimal(quantity) * unit_price * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
            if amount_cents <= 0:
                continue
            records.append(
                {
                    "transaction_id": f"{invoice}-{row['StockCode'].strip()}-{line_number}",
                    "event_timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "amount_cents": amount_cents,
                    "currency": "GBP",
                }
            )
    return records


def build_silver(records: list[dict]) -> list[dict]:
    """Validate raw records and retain the first occurrence of each transaction."""
    silver_records = []
    seen_transaction_ids = set()

    for record in records:
        missing_fields = [field for field in REQUIRED_FIELDS if not record.get(field)]
        if missing_fields:
            raise ValueError(f"missing required fields: {', '.join(missing_fields)}")
        if not isinstance(record["amount_cents"], int) or record["amount_cents"] <= 0:
            raise ValueError("amount_cents must be a positive integer")
        if record["transaction_id"] in seen_transaction_ids:
            continue

        seen_transaction_ids.add(record["transaction_id"])
        silver_records.append({field: record[field] for field in REQUIRED_FIELDS})

    return silver_records


def build_gold(records: list[dict]) -> list[dict]:
    """Aggregate de-duplicated Silver records by UTC event date and currency."""
    totals = defaultdict(lambda: {"transaction_count": 0, "total_amount_cents": 0})
    for record in build_silver(records):
        event_date = record["event_timestamp"][:10]
        key = (event_date, record["currency"])
        totals[key]["transaction_count"] += 1
        totals[key]["total_amount_cents"] += record["amount_cents"]

    return [
        {"event_date": event_date, "currency": currency, **totals[(event_date, currency)]}
        for event_date, currency in sorted(totals)
    ]
