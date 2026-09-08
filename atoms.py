import click
from pystow.utils import safe_open_writer

from build import get_basis_sets
from pathlib import Path
import pandas as pd

from curies import NamedReference

HERE = Path(__file__).parent.resolve()
URL = "https://github.com/cthoyt/chebi-atomic-numbers-ontology/raw/refs/heads/main/src/elements.tsv"
PATH = HERE.parent.joinpath("chebi-element-extension-ontology", "src", "elements.tsv")


def get_element_number_to_reference() -> dict[int, NamedReference]:
    df = pd.read_csv(PATH if PATH.is_file() else URL, sep="\t", skiprows=2, header=None,
                     names=['id', 'type', 'label', 'atomic number'])
    return {
        n: NamedReference.from_curie(curie, label.removesuffix(" atom"))
        for n, curie, label in df[['atomic number', 'id', "label"]].values
    }


@click.command()
def main() -> None:
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
