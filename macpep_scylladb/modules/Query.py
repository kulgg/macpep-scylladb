import logging
from typing import List
from cassandra.cqlengine import connection
from macpep_scylladb.database.Peptide import Peptide
from macpep_scylladb.modules.Partitioner import Partitioner
from macpep_scylladb.modules.Proteomics import Proteomics


class Query:
    def __init__(self, proteomics: Proteomics, partitioner: Partitioner):
        self.proteomics = proteomics
        self.partitioner = partitioner
        self.partitions = [
            0,
            644335421209,
            961537885881,
            1297732714404,
            1660711111977,
            2063197693248,
            2519216181507,
            3060541732774,
            3737901303107,
            4705032292661,
        ]

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
