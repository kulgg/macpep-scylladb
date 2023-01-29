[![build](https://github.com/kulgg/macpep-scylladb/actions/workflows/build.yml/badge.svg)](https://github.com/kulgg/macpep-scylladb/actions/workflows/build.yml)

# MaCPepDB - Mass Centric Peptide Database

Digests proteins stored in FASTA-/Uniprot-Text-files and inserts the resulting peptides and proteins into a ScyllaDB cluster.

## Getting started

Running with local docker compose Scylla cluster

1. Start Docker
2. `make up`
3. Wait for all scylla nodes to be UN with `make status`
4. Interact with app container `make app`
   - `cd app`
   - `poetry install`
   - `poetry run x` to run the CLI
