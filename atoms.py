import click
from pystow.utils import safe_open_writer

from build import get_basis_sets

ELEMENT_NUMBER_TO_CHEBI = {
    11: "26708",  # https://www.ebi.ac.uk/chebi/CHEBI:26708
}


@click.command()
def main() -> None:
    rows = []
    basis_sets = get_basis_sets()
    for basis_set in basis_sets:
        for element_number in basis_set.elements:
            identifier = ELEMENT_NUMBER_TO_CHEBI.get(element_number)
            if identifier is None:
                continue
            rows.append(
                (
                    basis_set.name,
                    element_number,
                    f"CHEBI:{identifier}",
                )
            )

    with safe_open_writer("atoms.tsv") as writer:
        writer.writerow(("basis set", "element", "element CURIE"))
        writer.writerows(rows)


if __name__ == "__main__":
    main()
