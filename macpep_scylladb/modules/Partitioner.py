import logging
from typing import List
from sortedcontainers import SortedList

from macpep_scylladb.modules.Proteomics import Proteomics
from macpep_scylladb.utils.UniprotTextReader import UniprotTextReader


class Partitioner:
    def __init__(self, proteomics: Proteomics):
        self.proteomics = proteomics

    def generate(self, num_partitions: int, uniprot_txt_path: str) -> List[int]:
        with open(uniprot_txt_path) as uniprot_file:
            reader = UniprotTextReader(uniprot_file)
            mass_list = SortedList()
            num_proteins = 0
            num_peptides = 0

            for protein in reader:
                num_proteins += 1
                for peptide_sequence in self.proteomics.digest(protein.sequence):
                    mass_list.add(self.proteomics.calculate_mass(peptide_sequence))
                    num_peptides += 1
                    if num_peptides % 100000 == 0:
                        logging.info("Processed %d peptides", num_peptides)

            num_peptides = len(mass_list)
            logging.info("Number of proteins: %d", num_proteins)
            logging.info("Number of peptides: %d", num_peptides)
            logging.info("Partitions: %d", num_partitions)
            peptides_per_partition = int(num_peptides / num_partitions)
            logging.info("Peptides per partition: %d", peptides_per_partition)

            partitions = [
                mass_list[i * peptides_per_partition] for i in range(num_partitions)
            ]
            partitions[0] = 0

            logging.info("Partition Distribution")
            for i in range(1, num_partitions):
                logging.info(
                    "[%d] %d <= mass < %d", i, partitions[i - 1], partitions[i]
                )
            logging.info("[%d] %d <= mass", num_partitions, partitions[-1])

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

    def get_partition_index_from_sequence(
        self, partitions: List[int], sequence: str
    ) -> int:
        return self.get_partition_index(
            partitions, self.proteomics.calculate_mass(sequence)
        )
