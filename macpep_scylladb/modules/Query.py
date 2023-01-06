import logging
import os
from typing import List
from cassandra.cqlengine import connection
from macpep_scylladb.database.Peptide import Peptide
from macpep_scylladb.modules.Partitioner import Partitioner
from macpep_scylladb.modules.Proteomics import Proteomics


class Query:
    def __init__(
        self,
        proteomics: Proteomics,
        partitioner: Partitioner,
        partitions_file_path: str = "data/partitions_1000.txt",
    ):
        self.proteomics = proteomics
        self.partitioner = partitioner
        self.partitions = []
        if os.path.exists(partitions_file_path):
            with open(partitions_file_path) as f:
                self.partitions = list(map(int, f.read().splitlines()))

    def peptides_by_sequence(self, server: str, sequence: str) -> List[Peptide]:
        connection.setup([server], "macpep")
        mass = self.proteomics.calculate_mass(sequence)
        logging.info("Mass %d", mass)
        partition = self.partitioner.get_partition_index(self.partitions, mass)
        logging.info("Partition %d", partition)
        peptides: List[Peptide] = []
        peptides.extend(
            Peptide.objects.filter(partition=partition, mass=mass, sequence=sequence)
        )
        logging.info(f"Found {len(peptides)} peptides with sequence {sequence}.")
        return peptides

    def peptides_by_mass(self, server: str, mass: int) -> List[Peptide]:
        connection.setup([server], "macpep")
        logging.info("Mass %d", mass)
        partition = self.partitioner.get_partition_index(self.partitions, mass)
        logging.info("Partition %d", partition)
        peptides: List[Peptide] = []
        peptides.extend(Peptide.objects.filter(partition=partition, mass=mass))
        logging.info(f"Found {len(peptides)} peptides with mass {mass}.")

        return peptides

    def peptides_by_mass_range(
        self, server: str, lower: int, upper: int
    ) -> List[Peptide]:
        connection.setup([server], "macpep")
        logging.info("Querying %d <= mass <= %d", lower, upper)
        lower_partition = self.partitioner.get_partition_index(self.partitions, lower)
        upper_partition = self.partitioner.get_partition_index(self.partitions, upper)
        logging.info("Partitions %d-%d", lower_partition, upper_partition)
        peptides: List[Peptide] = []
        for i in range(lower_partition, upper_partition + 1):
            peptides.extend(
                Peptide.objects.filter(partition=i, mass__gte=lower, mass__lte=upper)
            )
        logging.info(f"Found {len(peptides)} peptides")

        return peptides
