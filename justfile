format:
    ruff format
    ruff check --fix --unsafe-fixes .

terms:
    uv run \
      --script src/build.py \
      --output derived/basis-sets.tsv
    robot template \
      --prefix "dcterms: http://purl.org/dc/terms/" \
      --prefix "BSEO: http://purl.obolibrary.org/obo/BSEO_" \
      --prefix "CHEBI: http://purl.obolibrary.org/obo/CHEBI_" \
      --prefix "ORBITAL: http://w3id.org/biopragmatics/orbital/term/" \
      --prefix "ChEMROF: https://chemkg.github.io/chemrof/" \
      --template templates/roots.tsv \
      --template templates/properties.tsv \
      --template templates/families.tsv \
      --template templates/function-types.tsv \
      --template templates/roles.tsv \
      --template derived/basis-sets.tsv \
      --output derived/basis-sets.ofn

basis-set-to-element:
    uv run \
      --script src/basis_set_to_element.py \
      --output derived/basis-set-to-element.tsv
    robot template \
      --prefix "dcterms: http://purl.org/dc/terms/" \
      --prefix "BSEO: http://purl.obolibrary.org/obo/BSEO_" \
      --prefix "CHEBI: http://purl.obolibrary.org/obo/CHEBI_" \
      --prefix "ORBITAL: http://w3id.org/biopragmatics/orbital/term/" \
      --prefix "ChEMROF: https://chemkg.github.io/chemrof/" \
      --template templates/properties.tsv \
      --template derived/basis-set-to-element.tsv \
      --output derived/basis-set-to-element.ofn

build: terms basis-set-to-element
    robot merge \
        --input metadata.ttl \
        --input derived/basis-set-to-element.ofn \
        --input derived/basis-sets.ofn \
        --output bseo.ofn \
        --output bseo.owl
