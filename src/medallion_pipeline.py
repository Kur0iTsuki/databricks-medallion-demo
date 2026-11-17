"""A dependency-free, synthetic Medallion pipeline example."""

from collections import defaultdict


REQUIRED_FIELDS = ("transaction_id", "event_timestamp", "amount_cents", "currency")


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
