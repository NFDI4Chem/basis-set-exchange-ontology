format:
    ruff format
    ruff check --fix --unsafe-fixes .

basis-set-to-element:
    uv run \
      --script src/basis_set_to_element.py \
      --output output/basis-set-to_element.tsv
    robot template \
      --prefix "BSEO: http://purl.obolibrary.org/obo/BSEO_" \
      --prefix "CHEBI: http://purl.obolibrary.org/obo/CHEBI_" \
      --prefix "ORBITAL: http://w3id.org/biopragmatics/orbital/term/" \
      --prefix "ChEMROF: https://chemkg.github.io/chemrof/" \
      --template properties.tsv \
      --template output/basis-set-to_element.tsv \
      --output output/basis-set-to_element.ofn
