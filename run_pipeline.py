"""Run the synthetic Medallion example from the repository root."""

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "src"))

from medallion_pipeline import build_gold


def main() -> None:
    records = json.loads((Path(__file__).parent / "data" / "sample_transactions.json").read_text())
    print(json.dumps(build_gold(records), indent=2))


if __name__ == "__main__":
    main()
