"""Run the Medallion demo against Kaggle's CC0 Online Retail dataset."""

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "src"))

from medallion_pipeline import build_gold, load_online_retail_csv


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path, help="Path to Kaggle's Online_Retail.csv")
    arguments = parser.parse_args()

    records = load_online_retail_csv(arguments.csv_path)
    gold = build_gold(records)
    print(json.dumps({"purchase_lines": len(records), "daily_aggregates": len(gold), "preview": gold[:5]}, indent=2))


if __name__ == "__main__":
    main()
