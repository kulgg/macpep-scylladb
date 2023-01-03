import logging
from macpep_scylladb.database.Peptide import Peptide
from macpep_scylladb.modules.Cql import Cql
from macpep_scylladb.modules.Partitioner import Partitioner
from macpep_scylladb.modules.Proteomics import Proteomics
from macpep_scylladb.utils.UniprotTextReader import UniprotTextReader
from macpep_scylladb.utils.model_convert import to_database


class Inserter:
    def __init__(self, partitioner: Partitioner, proteomics: Proteomics, cql: Cql):
        self.partitioner = partitioner
        self.proteomics = proteomics
        self.cql = cql

    def run(self, server: str, partitions_file_path: str, uniprot_file_path: str):
        partitions_file = open(partitions_file_path, "r")
        partitions = list(map(int, partitions_file.read().splitlines()))
        logging.info(partitions)
        partitions_file.close()
        uniprot_f = open(uniprot_file_path, "r")
        reader = UniprotTextReader(uniprot_f)

        num_proteins = 0
        num_peptides = 0

        for protein in reader:
            num_proteins += 1
            protein_db = to_database(protein)
            self.cql.insert_protein(server, protein_db)
            for peptide_sequence in self.proteomics.digest(protein.sequence):
                mass = self.proteomics.calculate_mass(peptide_sequence)
                partition = self.partitioner.get_partition_index(partitions, mass)
                self.cql.upsert_peptide(
                    server,
                    Peptide(
                        partition=partition,
                        mass=mass,
                        sequence=peptide_sequence,
                        proteins={protein.sequence},
                        length=len(peptide_sequence),
                        number_of_missed_cleavages=0,
                        n_terminus=0,
                        c_terminus=0,
                    ),
                )
                num_peptides += 1
                if num_peptides % 100000 == 0:
                    logging.info("Processed %d peptides", num_peptides)

        logging.info("Number of proteins: %d", num_proteins)
        logging.info("Number of peptides: %d", num_peptides)

        uniprot_f.close()
