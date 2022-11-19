import logging
from typing import List
from sortedcontainers import SortedList

from macpep_scylladb.modules.Proteomics import Proteomics
from macpep_scylladb.utils.UniprotTextReader import UniprotTextReader


class Partitioner:
    def __init__(self, proteomics: Proteomics):
        self.proteomics = proteomics

    def generate_distribution(self, num_partitions: int, file_path: str) -> List[int]:
        with open(file_path) as uniprot_file:
            reader = UniprotTextReader(uniprot_file)
            mass_list = SortedList()

            for protein in reader:
                mass_list.add(self.proteomics.calculate_mass(protein.sequence))

            num_peptides = len(mass_list)
            logging.info("Total peptides: %d", num_peptides)
            peptides_per_partition = int(num_peptides / num_partitions)
            logging.info("Peptides per partition: %d", peptides_per_partition)

            partitions = [
                mass_list[i * peptides_per_partition] for i in range(num_partitions)
            ]

            # Double check partition sizes
            # for i in range(len(partitions)):
            #     count = 0
            #     for mass in mass_list:
            #         if mass >= partitions[i] and (
            #             i + 1 == len(partitions) or mass < partitions[i + 1]
            #         ):
            #             count += 1
            #     print(i, count)

            return partitions

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
