from pathlib import Path

from curies import NamedReference, Prefix
from pystow.utils import safe_open_dict_reader

__all__ = [
    "DERIVED_DIRECTORY",
    "HERE",
    "ROOT",
    "TEMPLATE_DIRECTORY",
    "TEMPORARY_DIRECTORY",
    "get_name_to_basis_set",
    "get_name_to_family",
    "get_name_to_function_type",
    "get_name_to_role",
]

PREFIX = Prefix("BSEO")

HERE = Path(__file__).parent.resolve()
ROOT = HERE.parent.resolve()
DEV_DIRECTORY = ROOT.parent.resolve()

TEMPORARY_DIRECTORY = ROOT / "tmp"
TEMPORARY_DIRECTORY.mkdir(parents=True, exist_ok=True)

DERIVED_DIRECTORY = ROOT.joinpath("derived")

TEMPLATE_DIRECTORY = ROOT.joinpath("templates")
FAMILIES_PATH = TEMPLATE_DIRECTORY.joinpath("families.tsv")
ROLES_PATH = TEMPLATE_DIRECTORY.joinpath("roles.tsv")
FUNCTION_TYPES_PATH = TEMPLATE_DIRECTORY.joinpath("function-types.tsv")
BASIS_SETS_PATH = TEMPLATE_DIRECTORY.joinpath("basis-sets.tsv")


def get_name_to_family() -> dict[str, NamedReference]:
    with safe_open_dict_reader(FAMILIES_PATH) as reader:
        next(reader)  # throw away second row, which is from robot template
        return {
            record["label"]: NamedReference.from_curie(
                record["curie"], name=record["label"]
            )
            for record in reader
        }


def get_name_to_role() -> dict[str, NamedReference]:
    with safe_open_dict_reader(ROLES_PATH) as reader:
        next(reader)  # throw away second row, which is from robot template
        return {
            record["label"]: NamedReference.from_curie(
                record["curie"], name=record["label"]
            )
            for record in reader
        }


def get_name_to_function_type() -> dict[str, NamedReference]:
    with safe_open_dict_reader(FUNCTION_TYPES_PATH) as reader:
        next(reader)  # throw away second row, which is from robot template
        return {
            record["abbreviation"]: NamedReference.from_curie(
                record["curie"], name=record["label"]
            )
            for record in reader
        }


def get_name_to_basis_set() -> dict[str, NamedReference]:
    with safe_open_dict_reader(BASIS_SETS_PATH) as reader:
        next(reader)  # throw away second row, which is from robot template
        return {
            record["label"]: NamedReference.from_curie(
                record["curie"], name=record["label"]
            )
            for record in reader
        }
