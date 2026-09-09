# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "click>=8.5.0",
#     "curies>=0.15.0",
#     "pandas>=3.0.5",
#     "pydantic>=2.13.5",
#     "pystow>=0.9.3",
#     "tabulate>=0.10.0",
#     "tqdm>=4.70.0",
# ]
# ///

from pathlib import Path

import click
import pandas as pd
from curies import NamedReference
from pystow.utils import safe_open_writer

from parse import iter_basis_sets

HERE = Path(__file__).parent.resolve()
ROOT = HERE.parent.resolve()
OUTPUT = ROOT.joinpath("output")
DEFAULT_OUTPUT_PATH = OUTPUT.joinpath("basis-set-to-element.tsv")

TERMS_PATH = ROOT.joinpath("derived-terms.tsv")

ELEMENTS_URL = "https://github.com/cthoyt/chebi-atomic-numbers-ontology/raw/refs/heads/main/src/elements.tsv"
ELEMENTS_PATH = HERE.parent.joinpath(
    "chebi-element-extension-ontology", "src", "elements.tsv"
)

ORBITALS_URL = (
    "https://github.com/cthoyt/orbital-ontology/raw/refs/heads/main/src/terms.tsv"
)
ORBITALS_PATH = HERE.parent.joinpath("orbital-ontology", "src", "terms.tsv")


def get_basis_set_to_reference() -> dict[str, NamedReference]:
    df = pd.read_csv(TERMS_PATH, sep="\t", skiprows=2, header=None, usecols=[0, 2])
    return {name: NamedReference.from_curie(curie, name) for curie, name in df.values}


def get_element_number_to_reference() -> dict[int, NamedReference]:
    df = pd.read_csv(
        ELEMENTS_PATH if ELEMENTS_PATH.is_file() else ELEMENTS_URL,
        sep="\t",
        skiprows=2,
        header=None,
        names=["id", "type", "label", "atomic number"],
    )
    return {
        n: NamedReference.from_curie(curie, label.removesuffix(" atom"))
        for n, curie, label in df[["atomic number", "id", "label"]].values
    }


def get_orbital_to_reference() -> dict[tuple[int, int, int], NamedReference]:
    """Get a mapping triples of principal, azimuthal, and magnetic quantum numbers to references."""
    df = pd.read_csv(
        ORBITALS_PATH if ORBITALS_PATH.is_file() else ORBITALS_URL,
        sep="\t",
        skiprows=2,
        header=None,
        usecols=[0, 2, 7, 8, 9],
        names=["identifier", "label", "principal", "azimuthal", "magnetic"],
        dtype=str,
    )
    df = df[df["principal"].notna() & df["azimuthal"].notna() & df["magnetic"].notna()]
    for key in ["principal", "azimuthal", "magnetic"]:
        df[key] = df[key].astype(int)
    return {
        (n, l, m_l): NamedReference.from_curie(curie, name)
        for curie, name, n, l, m_l in df.values
    }


@click.command()
@click.option("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
def main(output: Path) -> None:
    basis_set_to_reference = get_basis_set_to_reference()
    element_number_to_reference = get_element_number_to_reference()
    rows = []
    for basis_set in iter_basis_sets():
        basis_set_reference = basis_set_to_reference[basis_set.name]
        for element_number in basis_set.elements:
            reference = element_number_to_reference[element_number]
            rows.append(
                (
                    basis_set_reference.curie,
                    "class",
                    basis_set.name,
                    element_number,
                    reference.curie,
                    reference.name,
                )
            )

    with safe_open_writer(output) as writer:
        writer.writerow(
            ("ID", "TYPE", "basis set", "element", "element CURIE", "element name")
        )
        writer.writerow(("ID", "TYPE", "", "", "SC 'BSEO:1000003' some %", ""))
        writer.writerows(rows)


if __name__ == "__main__":
    main()
