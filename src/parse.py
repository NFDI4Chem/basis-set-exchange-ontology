import datetime
import json
import tarfile
from collections.abc import Iterable
from typing import Annotated, Any, Literal, TypeAlias

import pystow
from pydantic import BaseModel, BeforeValidator
from tqdm import tqdm

__all__ = [
    "FUNCTION_TYPE_NAMES",
    "BasisSet",
    "ECPPotential",
    "ECPPotentialRecord",
    "ElectronShell",
    "ElectronShellRecord",
    "FunctionType",
    "Region",
    "iter_basis_sets",
]


def _f(s: str | None) -> str | None:
    if s is not None and s.strip():
        return s.strip()
    return None


ElectronShellFunctionType: TypeAlias = Literal["gto", "gto_spherical", "gto_cartesian"]
FunctionType = ElectronShellFunctionType | Literal["scalar_ecp"]
Region: TypeAlias = Literal["valence", "diffuse", "polarization"]


class ElectronShell(BaseModel):
    function_type: ElectronShellFunctionType
    region: Annotated[Region | None, BeforeValidator(_f)] = None
    # something fishy is going on here, should not go past 6
    angular_momentum: list[Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    exponents: list[str]
    coefficients: list[list[str]]


class ElectronShellRecord(BaseModel):
    electron_shells: list[ElectronShell]
    references: list[dict[str, Any]]


class ECPPotential(BaseModel):
    ecp_type: Literal["scalar_ecp"]  # TODO reroute into "function_type"
    r_exponents: list[int]
    gaussian_exponents: list[float]
    angular_momentum: list[int]
    exponents: list[str] | None = None
    coefficients: list[list[str]]


class ECPPotentialRecord(BaseModel):
    ecp_potentials: list[ECPPotential]
    ecp_electrons: int
    references: list[dict[str, Any]]


class BasisSet(BaseModel):
    name: str
    role: str
    description: str
    family: str
    function_types: list[str]
    tags: list[str]
    # TODO auxiliaries
    # TODO names
    elements: dict[int, ElectronShellRecord | ECPPotentialRecord]
    revision_date: datetime.date
    revision_description: str
    version: str


#: A mapping from function type to names
FUNCTION_TYPE_NAMES: dict[FunctionType, str] = {
    "gto": "Gaussian-type orbitals",
    "gto_spherical": "spherical Gaussian-type orbitals",
    "gto_cartesian": "cartesian Gaussian-type orbitals",
    "scalar_ecp": "scalar effective core potentials",
}

DEFAULT_VERSION = "0.12"
MODULE = pystow.module("bio", "basis-set-exchange")


def get_download_url(version: str) -> str:
    """Get the download URL for the given version."""
    return f"https://www.basissetexchange.org/static/archives/{version}/basis_sets-json-{version}.tar.bz2"


def iter_basis_sets(
    *, force: bool = False, version: str | None = None
) -> Iterable[BasisSet]:
    """Parse basis sets from the zipped file."""
    url = get_download_url(version or DEFAULT_VERSION)
    path = MODULE.ensure(url=url, force=force)
    seen = set()
    # TODO get clever to only keep the latest version of each
    with tarfile.open(path) as tf:
        for member in tqdm(tf, unit="file"):
            if not member.name.endswith(".json"):
                continue
            with tf.extractfile(member) as file:
                data = json.load(file)
            yv = BasisSet.model_validate(data)
            if yv.name in seen:
                continue
            seen.add(yv.name)
            yield yv
