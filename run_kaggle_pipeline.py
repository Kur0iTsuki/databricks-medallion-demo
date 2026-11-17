"""Run the Medallion demo against Kaggle's CC0 Online Retail dataset."""

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "src"))

from medallion_pipeline import build_gold, load_online_retail_csv

DEFAULT_CSV_PATH = Path("data/raw/Online_Retail.csv")


def resolve_csv_path(csv_path: Path | None) -> Path:
    """Return the supplied source file or explain how to obtain the default one."""
    resolved_path = csv_path or DEFAULT_CSV_PATH
    if not resolved_path.is_file():
        raise FileNotFoundError(
            f"Dataset not found at {resolved_path}. "
            "Run `sh scripts/download_kaggle_dataset.sh` first, or pass the CSV path explicitly."
        )
    return resolved_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "csv_path",
        type=Path,
        nargs="?",
        help="Optional path to Kaggle's Online_Retail.csv (defaults to data/raw/Online_Retail.csv)",
    )
    arguments = parser.parse_args()

    records = load_online_retail_csv(resolve_csv_path(arguments.csv_path))
    gold = build_gold(records)
    print(json.dumps({"purchase_lines": len(records), "daily_aggregates": len(gold), "preview": gold[:5]}, indent=2))


if __name__ == "__main__":
    main()
