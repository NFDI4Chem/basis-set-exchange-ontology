from pathlib import Path

import click
import pandas as pd
from curies import NamedReference
from pystow.utils import safe_open_writer

from build import get_basis_sets

HERE = Path(__file__).parent.resolve()
ELEMENTS_URL = "https://github.com/cthoyt/chebi-atomic-numbers-ontology/raw/refs/heads/main/src/elements.tsv"
ELEMENTS_PATH = HERE.parent.joinpath(
    "chebi-element-extension-ontology", "src", "elements.tsv"
)

ORBITALS_URL = (
    "https://github.com/cthoyt/orbital-ontology/raw/refs/heads/main/src/terms.tsv"
)
ORBITALS_PATH = HERE.parent.joinpath("orbital-ontology", "src", "terms.tsv")


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
def main() -> None:
    orbital_to_reference = get_orbital_to_reference()
    element_number_to_reference = get_element_number_to_reference()
    rows = []
    basis_sets = get_basis_sets()
    for basis_set in basis_sets:
        for element_number in basis_set.elements:
            reference = element_number_to_reference[element_number]
            rows.append(
                (
                    basis_set.name,
                    element_number,
                    reference.curie,
                    reference.name,
                )
            )

    with safe_open_writer("atoms.tsv") as writer:
        writer.writerow(("basis set", "element", "element CURIE", "element name"))
        writer.writerows(rows)


if __name__ == "__main__":
    main()
