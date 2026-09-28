# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "curies>=0.15.0",
#     "pandas>=3.0.5",
#     "pystow>=0.9.3",
# ]
# ///

"""Lint curated data files."""

import pandas as pd

from utils import TEMPLATE_DIRECTORY

SORT = {
    "basis-set-parents": "curie"
}


def main() -> None:
    """Lint curated data files."""
    for path in TEMPLATE_DIRECTORY.glob("*.tsv"):
        if path.name.endswith("sssom.tsv"):
            continue
        df = pd.read_csv(path, sep="\t", dtype=str)

        for col in df.columns:
            df[col] = df[col].map(str.strip, na_action="ignore")

        if sort := SORT.get(path.name):
            df.iloc[1:] = df.iloc[1:].sort_values(sort)

        df.to_csv(path, index=False, sep="\t", encoding="utf-8")


if __name__ == "__main__":
    main()
