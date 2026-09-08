build:
    uv run --script atoms.py
    robot template \
      --prefix "BSEO: http://purl.obolibrary.org/obo/BSEO_" \
      --prefix "CHEBI: http://purl.obolibrary.org/obo/CHEBI_" \
      --prefix "ORBITAL: http://w3id.org/biopragmatics/orbital/term/" \
      --prefix "ChEMROF: https://chemkg.github.io/chemrof/" \
      --template properties.tsv \
      --template atoms.tsv \
      --output atoms.owl
