import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from medallion_pipeline import build_gold, build_silver


class MedallionPipelineTests(unittest.TestCase):
    def test_build_silver_rejects_invalid_amounts(self):
        records = [
            {
                "transaction_id": "txn-100",
                "event_timestamp": "2026-01-01T10:00:00Z",
                "amount_cents": 0,
                "currency": "USD",
            }
        ]

        with self.assertRaisesRegex(ValueError, "amount_cents"):
            build_silver(records)

    def test_build_gold_deduplicates_before_daily_aggregation(self):
        records = [
            {
                "transaction_id": "txn-100",
                "event_timestamp": "2026-01-01T10:00:00Z",
                "amount_cents": 1250,
                "currency": "USD",
            },
            {
                "transaction_id": "txn-100",
                "event_timestamp": "2026-01-01T11:00:00Z",
                "amount_cents": 1250,
                "currency": "USD",
            },
            {
                "transaction_id": "txn-101",
                "event_timestamp": "2026-01-01T12:00:00Z",
                "amount_cents": 275,
                "currency": "USD",
            },
        ]

        self.assertEqual(
            build_gold(records),
            [{"event_date": "2026-01-01", "currency": "USD", "transaction_count": 2, "total_amount_cents": 1525}],
        )


if __name__ == "__main__":
    unittest.main()
