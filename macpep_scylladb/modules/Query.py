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
    ):
        self.proteomics = proteomics
        self.partitioner = partitioner
        self.partitions = []
        self.current_partitions_path = ""
        self.is_connection_setup = False

    def _set_partitions(self, partitions_file_path: str):
        if self.current_partitions_path == partitions_file_path:
            return

        if os.path.exists(partitions_file_path):
            with open(partitions_file_path) as f:
                self.partitions = list(map(int, f.read().splitlines()))
            self.current_partitions_path = partitions_file_path
        else:
            raise Exception("Not a valid path")

    def _setup_connection(self, server: str):
        if not self.is_connection_setup:
            connection.setup([server], "macpep")
            self.is_connection_setup = True

    def peptides_by_sequence(
        self, server: str, sequence: str, partitions_file_path: str
    ) -> List[Peptide]:
        self._set_partitions(partitions_file_path)
        self._setup_connection(server)
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

    def peptides_by_mass(
        self, server: str, mass: int, partitions_file_path: str
    ) -> List[Peptide]:
        self._set_partitions(partitions_file_path)
        self._setup_connection(server)
        logging.info("Mass %d", mass)
        partition = self.partitioner.get_partition_index(self.partitions, mass)
        logging.info("Partition %d", partition)
        peptides: List[Peptide] = []
        peptides.extend(Peptide.objects.filter(partition=partition, mass=mass))
        logging.info(f"Found {len(peptides)} peptides with mass {mass}.")

        return peptides

    def peptides_by_mass_range(
        self, server: str, lower: int, upper: int, partitions_file_path: str
    ) -> List[Peptide]:
        self._set_partitions(partitions_file_path)
        self._setup_connection(server)
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
