format:
    ruff format
    ruff check --fix --unsafe-fixes .

terms:
    uv run --script src/build_new.py

basis-set-to-element:
    uv run \
      --script src/basis_set_to_element.py \
      --output derived/basis-set-to-element.tsv
    robot template \
      --prefix "BSEO: http://purl.obolibrary.org/obo/BSEO_" \
      --prefix "CHEBI: http://purl.obolibrary.org/obo/CHEBI_" \
      --prefix "ORBITAL: http://w3id.org/biopragmatics/orbital/term/" \
      --prefix "ChEMROF: https://chemkg.github.io/chemrof/" \
      --template properties.tsv \
      --template derived/basis-set-to-element.tsv \
      --output derived/basis-set-to-element.ofn

build: manual-subclasses terms
    robot merge \
        --input derived/basis-set-to-element.ofn \
        --input bseo.owl \
        --output bseo.ofn \
        --output bseo.owl
