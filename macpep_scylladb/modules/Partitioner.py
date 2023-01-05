from collections import defaultdict
import collections
import logging
import os
from typing import List, Dict, OrderedDict

from macpep_scylladb.modules.Proteomics import Proteomics
from macpep_scylladb.utils.UniprotTextReader import UniprotTextReader
from macpep_scylladb.utils.rolling_set import RollingSet


class Partitioner:
    def __init__(self, proteomics: Proteomics):
        self.proteomics = proteomics

    def _get_partitions(
        self,
        num_partitions: int,
        num_peptides: int,
        peptides_per_mass: OrderedDict[int, int],
    ) -> List[int]:
        peptides_per_partition = int(num_peptides / num_partitions)
        logging.info("Peptides per partition: %d", peptides_per_partition)

        partitions = [0]
        counter = 0
        for mass, count in peptides_per_mass.items():
            counter += count
            if counter >= peptides_per_partition:
                partitions.append(mass)
                counter = 0
        return partitions

    def _get_peptide_counts(self, partitions, peptides_per_mass):
        num_partitions = len(partitions)
        peptide_counts = [0] * num_partitions
        for mass, count in peptides_per_mass.items():
            for i in range(num_partitions):
                if mass >= partitions[i] and (
                    i + 1 == num_partitions or mass < partitions[i + 1]
                ):
                    peptide_counts[i] += count
        return peptide_counts

    def generate(
        self,
        num_partitions: int,
        uniprot_txt_path: str,
        partitions_path: str = "data/partitions.txt",
        rolling_set_maxsize: int = 100000,
    ) -> None:
        with open(uniprot_txt_path) as uniprot_file:
            reader = UniprotTextReader(uniprot_file)
            peptides_per_mass: Dict[int, int] = defaultdict(int)
            num_proteins = 0
            num_peptides = 0
            num_unique_peptides = 0
            seen_peptides = RollingSet(rolling_set_maxsize)

            for protein in reader:
                num_proteins += 1
                for peptide_sequence, num_of_missed_cleavages in self.proteomics.digest(
                    protein.sequence
                ):
                    num_peptides += 1
                    if peptide_sequence not in seen_peptides:
                        seen_peptides.add(peptide_sequence)
                        mass = self.proteomics.calculate_mass(peptide_sequence)
                        peptides_per_mass[mass] += 1
                        num_unique_peptides += 1
                    if num_peptides % 100000 == 0:
                        logging.info("Processed %d peptides", num_peptides)

            logging.info("Number of proteins: %d", num_proteins)
            logging.info("Number of peptides: %d", num_peptides)
            logging.info("Number of unique peptides: %d", num_unique_peptides)
            logging.info("Partitions: %d", num_partitions)

            od_peptides_per_mass = collections.OrderedDict(
                sorted(peptides_per_mass.items())
            )

            partitions = self._get_partitions(
                num_partitions, num_peptides, od_peptides_per_mass
            )

            num_partitions = len(partitions)
            logging.info("Actual partitions length: %d", num_partitions)

            peptide_counts = self._get_peptide_counts(partitions, od_peptides_per_mass)

            for i in range(num_partitions):
                logging.info("Partition %d: %d peptides", i, peptide_counts[i])

            os.makedirs(os.path.dirname(partitions_path), exist_ok=True)
            with open(partitions_path, "w") as f:
                for partition in partitions:
                    f.write(f"{partition}\n")

    def get_partition_index(self, partitions: List[int], mass: int) -> int:
        start, end = 0, len(partitions) - 1

        while start <= end:
            mid = (start + end) // 2
            if mass >= partitions[mid] and (
                mid + 1 == len(partitions) or mass < partitions[mid + 1]
            ):
                return mid
            if mass >= partitions[mid]:
                start = mid + 1
            else:
                end = mid - 1

        return -1

    def get_partition_index_from_sequence(
        self, partitions: List[int], sequence: str
    ) -> int:
        return self.get_partition_index(
            partitions, self.proteomics.calculate_mass(sequence)
        )
