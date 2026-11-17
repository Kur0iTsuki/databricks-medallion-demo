import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from medallion_pipeline import build_gold, build_silver, load_online_retail_csv


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

    def test_load_online_retail_csv_creates_line_level_records(self):
        source = (
            "InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,CustomerID,Country\n"
            "536365,85123A,WHITE HANGING HEART T-LIGHT HOLDER,6,12/1/10 8:26,2.55,17850,United Kingdom\n"
            "C536366,71053,RETURNED ITEM,-1,12/1/10 8:28,3.39,17850,United Kingdom\n"
            "536414,22139,FRACTIONAL ADJUSTMENT,1,12/1/10 11:52,0.001,17850,United Kingdom\n"
        )
        with tempfile.NamedTemporaryFile("w", suffix=".csv") as dataset:
            dataset.write(source)
            dataset.flush()
            records = load_online_retail_csv(Path(dataset.name))

        self.assertEqual(
            records,
            [
                {
                    "transaction_id": "536365-85123A-1",
                    "event_timestamp": "2010-12-01T08:26:00Z",
                    "amount_cents": 1530,
                    "currency": "GBP",
                }
            ],
        )

    def test_load_online_retail_csv_accepts_latin_1_product_descriptions(self):
        source = (
            "InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,CustomerID,Country\n"
            "536365,85123A,GIFT VOUCHER £40,1,12/1/10 8:26,40.00,17850,United Kingdom\n"
        )
        with tempfile.NamedTemporaryFile("w", suffix=".csv", encoding="latin-1") as dataset:
            dataset.write(source)
            dataset.flush()
            records = load_online_retail_csv(Path(dataset.name))

        self.assertEqual(records[0]["amount_cents"], 4000)


if __name__ == "__main__":
    unittest.main()
