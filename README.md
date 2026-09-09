# Basis Set Exchange Ontology

A [basis set](https://en.wikipedia.org/wiki/Basis_set_%28chemistry%29) is a set
of mathematical functions and their respective parametrization used to construct
a wave equation in computational chemistry experiments.

The [Basis Set Exchange](https://www.basissetexchange.org) is a comprehensive
database of basis sets. However, it does not provide persistent identifiers for
basis sets, does not provide an ontologization of basis sets beyond
categorization by _role_, and does not provide a semantic web-ready artifact.

The high level goals of this repository are to:

1. Enable the FAIR annotation of the basis sets used in computational chemistry
   experiments
2. Enable researchers to identify basis sets over several axes both in informal
   settings and with the assistance of reasoners

We want to accomplish the following technical goals to get there:

1. Automatically assign well-formed identifiers to each basis set in the Basis
   Set Exchange
2. Capture a deeper hierarchy of basis sets (e.g., by family and subfamily)
3. Capture the logical construction of each basis set (e.g., usage of diffusion
   function, usage of polarization function)

## License

Code in this repository is licensed under the MIT license. Original data is
licensed under CC0-1.0. Content derived from the Basis Set Exchange is licensed
under the BSD license
([reference](https://github.com/MolSSI-BSE/basis_set_exchange)).

## Contributing

### Exploration

Naming of basis sets is complicated! Take `aug-cc-pVTZ`:

| Part | Meaning                       |
| ---- | ----------------------------- |
| aug  | augmented (diffuse functions) |
| cc   | correlation-consistent        |
| p    | polarized                     |
| V    | valence-only correlation      |
| TZ   | triple-zeta                   |

Roles:

| role    | count |
| ------- | ----- |
| orbital | 804   |
| rifit   | 67    |
| optri   | 21    |
| jkfit   | 10    |
| admmfit | 6     |
| jfit    | 6     |
| guess   | 4     |
| dftjfit | 2     |
| dftxfit | 2     |

Families:

| family          | count |
| --------------- | ----- |
| jensen          | 120   |
| dunning         | 82    |
| ahlrichs        | 49    |
| dunning_fit     | 46    |
| pople           | 42    |
| jorge           | 37    |
| ano             | 35    |
| dunning_dk      | 34    |
| ranasinghe      | 25    |
| lehtola_hgbs    | 24    |
| dunning_pp_fit  | 24    |
| dunning_sf      | 24    |
| dyall           | 24    |
| sapporo         | 24    |
| ahlrichs_x2c    | 24    |
| dunning_pp      | 16    |
| sigmanz         | 15    |
| dunning_hay     | 14    |
| ahlrichs_fit    | 13    |
| truhlar         | 12    |
| dunning_x2c     | 12    |
| binning         | 12    |
| pb              | 12    |
| dunning_f12     | 11    |
| lehtola_emd     | 11    |
| lanl            | 11    |
| sarc            | 10    |
| sto             | 10    |
| ano_claudino    | 9     |
| dunning_f12_fit | 9     |
| huzinaga        | 8     |
| sauer_j         | 7     |
| dgauss          | 7     |
| ahlrichs_dhf    | 7     |
| dunning_dk3     | 6     |
| aug_mcc         | 6     |
| pople_mod       | 6     |
| nasa            | 6     |
| stuttgart       | 6     |
| dfo             | 5     |
| jgauss          | 5     |
| paw             | 5     |
| zorrilla        | 4     |
| ccj             | 4     |
| crenb           | 4     |
| partridge       | 4     |
| pob             | 4     |
| sbkjc           | 4     |
| sadlej          | 4     |
| lehtola_sap     | 4     |
| acvxz-j         | 3     |
| paschoal        | 3     |
| psx             | 3     |
| pople_fit       | 2     |
| blaudeau        | 2     |
| iglo            | 2     |
| pec             | 2     |
| cadpac          | 1     |
| cologne         | 1     |
| demon2k         | 1     |
| grimme          | 1     |
| koga            | 1     |
| orp             | 1     |
| ugbs            | 1     |
| wachters        | 1     |

Function Types:

| function type | count |
| ------------- | ----- |
| gto           | 913   |
| gto_spherical | 865   |
| scalar_ecp    | 109   |
| gto_cartesian | 30    |
