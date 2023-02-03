import logging
import os
from typing import Awaitable, List, Tuple

from cassandra.cluster import Cluster

from macpep_scylladb.database.Peptide import Peptide
from macpep_scylladb.modules.Partitioner import Partitioner
from macpep_scylladb.modules.Proteomics import Proteomics
from macpep_scylladb.utils.queries import (
    prepare_peptide_query,
    query_peptides,
    query_peptides_list,
)


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
        self.session = None
        self.prepared_statements = dict()

    def _set_partitions(self, partitions_file_path: str):
        if self.current_partitions_path == partitions_file_path:
            return

        if os.path.exists(partitions_file_path):
            with open(partitions_file_path) as f:
                self.partitions = list(map(int, f.read().splitlines()))
            self.current_partitions_path = partitions_file_path
        else:
            raise Exception("Not a valid path")

    # def _setup_connection(self, server: str):
    #     if not self.is_connection_setup:
    #         connection.setup([server], "macpep")
    #         self.is_connection_setup = True

    def _setup_cluster(self, servers: List[str]):
        if not self.session:
            cluster = Cluster(servers)
            self.session = cluster.connect("macpep")

    # def peptides_by_sequence(
    #     self, server: str, sequence: str, partitions_file_path: str
    # ) -> List[Peptide]:
    #     self._set_partitions(partitions_file_path)
    #     self._setup_connection(server)
    #     mass = self.proteomics.calculate_mass(sequence)
    #     logging.info("Mass %d", mass)
    #     partition = self.partitioner.get_partition_index(self.partitions, mass)
    #     logging.info("Partition %d", partition)
    #     peptides: List[Peptide] = []
    #     peptides.extend(
    #         Peptide.objects.filter(partition=partition, mass=mass, sequence=sequence)
    #     )
    #     logging.info(f"Found {len(peptides)} peptides with sequence {sequence}.")
    #     return peptides

    # def peptides_by_mass(
    #     self, server: str, mass: int, partitions_file_path: str
    # ) -> List[Peptide]:
    #     self._set_partitions(partitions_file_path)
    #     self._setup_connection(server)
    #     logging.info("Mass %d", mass)
    #     partition = self.partitioner.get_partition_index(self.partitions, mass)
    #     logging.info("Partition %d", partition)
    #     peptides: List[Peptide] = []
    #     peptides.extend(Peptide.objects.filter(partition=partition, mass=mass))
    #     logging.info(f"Found {len(peptides)} peptides with mass {mass}.")

    #     return peptides

    def peptides_by_mass_range(
        self, servers: str, lower: int, upper: int, partitions_file_path: str
    ) -> List[Awaitable]:
        self._set_partitions(partitions_file_path)
        self._setup_cluster(servers)
        if "peptides_by_mass_range" not in self.prepared_statements:
            logging.info("Preparing statement")
            self.prepared_statements["peptides_by_mass_range"] = prepare_peptide_query(
                self.session
            )
        lower_partition = self.partitioner.get_partition_index(self.partitions, lower)
        upper_partition = self.partitioner.get_partition_index(self.partitions, upper)
        total = 0
        for i in range(lower_partition, upper_partition + 1):
            total += len(
                list(
                    query_peptides(
                        self.session,
                        self.prepared_statements["peptides_by_mass_range"],
                        i,
                        lower,
                        upper,
                    )
                )
            )
        return total

    def peptides_by_mass_range_list(
        self,
        servers: str,
        lowerUpperList: List[Tuple[int, int]],
        partitions_file_path: str,
    ) -> List[Awaitable]:
        self._set_partitions(partitions_file_path)
        self._setup_cluster(servers)
        if "peptides_by_mass_range" not in self.prepared_statements:
            logging.info("Preparing statement")
            self.prepared_statements["peptides_by_mass_range"] = prepare_peptide_query(
                self.session
            )

        params = []
        for lower, upper in lowerUpperList:
            lower_partition = self.partitioner.get_partition_index(
                self.partitions, lower
            )
            upper_partition = self.partitioner.get_partition_index(
                self.partitions, upper
            )
            for i in range(lower_partition, upper_partition + 1):
                params.append((i, lower, upper))

        results = query_peptides_list(
            self.session,
            self.prepared_statements["peptides_by_mass_range"],
            params,
        )

        total = 0
        for success, result in results:
            if not success:
                raise Exception(result)  # result will be an Exception
            else:
                total += len(list(result))

        return total
