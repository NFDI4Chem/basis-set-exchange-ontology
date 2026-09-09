# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "click",
#     "curies>=0.15.0",
#     "pydantic>=2.13.5",
#     "pystow>=0.9.3",
#     "tqdm>=4.70.0",
# ]
# ///

import sys
from pathlib import Path

import click
from curies import NamedReference, Prefix
from pystow.utils import safe_open_writer

from parse import iter_basis_sets
from utils import (
    DERIVED_DIRECTORY,
    get_name_to_basis_set,
    get_name_to_family,
    get_name_to_function_type,
    get_name_to_role,
)

BASIS_SET_PATH = DERIVED_DIRECTORY.joinpath("basis-sets.tsv")
BASIS_SET_HEADER_1 = (
    "curie",
    "type",
    "label",
    "parent",
    "parent label",
    "role",
    "role label",
    "function types",
    "description",
    "modified date",
)
BASIS_SET_HEADER_2 = (
    "ID",
    "TYPE",
    "AT rdfs:label^^xsd:string",
    "SC %",
    "",
    "SC 'has role' some %",
    "",
    "SC 'has function type' some % SPLIT=|",
    "AT dcterms:description^^xsd:string",
    "AT dcterms:modified^^xsd:date",
)

BASIS_SET_FUNCTIONS_PATH = DERIVED_DIRECTORY.joinpath("basis-set-functions.tsv")

URI_PREFIX = "https://www.basissetexchange.org/notes/"
PREFIX = Prefix("BSEO")


def _r(identifier: str, name: str) -> NamedReference:
    return NamedReference(prefix=PREFIX, identifier=identifier, name=name)


@click.command()
@click.option("--output", default=BASIS_SET_PATH)
def main(output: Path) -> None:
    families = get_name_to_family()
    roles = get_name_to_role()
    function_types = get_name_to_function_type()
    basis_sets = get_name_to_basis_set()
    with safe_open_writer(output) as writer:
        writer.writerow(BASIS_SET_HEADER_1)
        writer.writerow(BASIS_SET_HEADER_2)
        for basis_set in iter_basis_sets():
            basis_set_reference = basis_sets.get(basis_set.name)
            if basis_set_reference is None:
                click.secho(
                    "basis sets in templates/basis-sets.tsv need to be extended"
                )
                sys.exit(0)
            writer.writerow(
                (
                    basis_set_reference.curie,
                    "class",
                    basis_set.name,  # label
                    families[basis_set.family].curie,  # parent
                    basis_set.family,  # parent label
                    roles[basis_set.role].curie,  # role
                    basis_set.role,  # role label
                    "|".join(
                        function_types[function_type].curie
                        for function_type in basis_set.function_types or []
                    ),
                    basis_set.description
                    if basis_set.description and basis_set.description != basis_set.name
                    else "",
                    basis_set.revision_date.isoformat(),
                )
            )


if __name__ == "__main__":
    main()
