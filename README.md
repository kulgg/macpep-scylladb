[![build](https://github.com/kulgg/macpep-scylladb/actions/workflows/build.yml/badge.svg)](https://github.com/kulgg/macpep-scylladb/actions/workflows/build.yml)

# MaCPepDB - Mass Centric Peptide Database

Digests proteins stored in FASTA-/Uniprot-Text-files and inserts the resulting peptides and proteins into a ScyllaDB cluster.

ToDo:

- [x] Add function to digest protein sequence with enzyme
- [ ] Add module for creating the protein/peptide schema in scylladb
- [ ] Add module with main insertion loop (from uniprot txt into the db)
