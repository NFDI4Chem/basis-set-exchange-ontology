# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "curies>=0.15.0",
#     "pydantic>=2.13.5",
#     "pystow>=0.9.3",
#     "tqdm>=4.70.0",
# ]
# ///

from curies import NamedReference, Prefix
from pystow.utils import safe_open_writer

from parse import iter_basis_sets
from utils import DERIVED_DIRECTORY, get_name_to_function_type, get_name_to_role, get_name_to_family

BASIS_SET_PATH = DERIVED_DIRECTORY.joinpath("basis-sets.tsv")
BASIS_SET_HEADER_1 = ("curie", "type", "label", "parent", "parent label", "role", "role label", "function types", "description")
BASIS_SET_HEADER_2 = (
    "ID",
    "TYPE",
    "AT rdfs:label^^xsd:string",
    "SC %",
    "",
    "SC %",
    "",
    "SC % SPLIT=|",
    "AT dcterms:description^^xsd:string",
)

BASIS_SET_FUNCTIONS_PATH = DERIVED_DIRECTORY.joinpath("basis-set-functions.tsv")

URI_PREFIX = "https://www.basissetexchange.org/notes/"
PREFIX = Prefix("BSEO")


def _r(identifier: str, name: str) -> NamedReference:
    return NamedReference(prefix=PREFIX, identifier=identifier, name=name)


def main() -> None:
    families = get_name_to_family()
    roles = get_name_to_role()
    function_types = get_name_to_function_type()

    basis_sets = list(iter_basis_sets())

    with safe_open_writer(BASIS_SET_PATH) as writer:
        writer.writerow(BASIS_SET_HEADER_1)
        writer.writerow(BASIS_SET_HEADER_2)
        for i, basis_set in enumerate(basis_sets, start=1):
            writer.writerow(
                (
                    f"BSEO:{i:07}",
                    "class",
                    basis_set.name,  # label
                    families[basis_set.family].curie,  # parent
                    basis_set.family,  # parent label
                    roles[basis_set.role].curie,  # role
                    basis_set.role,  # role label
                    " | ".join(
                        function_types[function_type].curie
                        for function_type in basis_set.function_types or []
                    ),
                    basis_set.description
                    if basis_set.description and basis_set.description != basis_set.name
                    else "",
                )
            )


if __name__ == "__main__":
    main()
