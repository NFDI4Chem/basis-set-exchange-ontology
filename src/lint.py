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


def main() -> None:
    """Lint curated data files."""
    for path in TEMPLATE_DIRECTORY.glob("*.tsv"):
        df = pd.read_csv(path, sep="\t")
        df.to_csv(path, index=False, sep="\t")


if __name__ == "__main__":
    main()
