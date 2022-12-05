from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, wait
import logging
import os
import threading
from typing import List, Dict

from macpep_scylladb.modules.Proteomics import Proteomics
from macpep_scylladb.utils.UniprotTextReader import UniprotTextReader


class Partitioner:
    def __init__(self, proteomics: Proteomics):
        self.proteomics = proteomics

    def _get_partitions(
        self, num_partitions: int, num_peptides: int, peptides_per_mass: Dict[int, int]
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

    def _get_peptide_counts(num_partitions, partitions, peptides_per_mass):
        peptide_counts = [0] * num_partitions
        for mass, count in peptides_per_mass.items():
            for i in range(num_partitions):
                if mass >= partitions[i] and (
                    i + 1 == num_partitions or mass < partitions[i + 1]
                ):
                    peptide_counts[i] += count
        return peptide_counts

    def generate(self, num_partitions: int, uniprot_txt_path: str) -> List[int]:
        with open(uniprot_txt_path) as uniprot_file:
            reader = UniprotTextReader(uniprot_file)
            peptides_per_mass: Dict[int, int] = defaultdict(int)
            num_proteins = 0
            num_peptides = 0

            for protein in reader:
                num_proteins += 1
                for peptide_sequence in self.proteomics.digest(protein.sequence):
                    mass = self.proteomics.calculate_mass(peptide_sequence)
                    peptides_per_mass[mass] += 1
                    num_peptides += 1
                    if num_peptides % 100000 == 0:
                        logging.info("Processed %d peptides", num_peptides)

            logging.info("Number of proteins: %d", num_proteins)
            logging.info("Number of peptides: %d", num_peptides)
            logging.info("Partitions: %d", num_partitions)

            partitions = self._get_partitions(
                num_partitions, num_peptides, peptides_per_mass
            )

            peptide_counts = self._get_peptide_counts(
                num_partitions, partitions, peptides_per_mass
            )

            for i in range(num_partitions):
                logging.info("Partition %d: %d peptides", i, peptide_counts[i])

            out_file_path = "out/partitions.txt"
            os.makedirs(os.path.dirname(out_file_path), exist_ok=True)
            with open(out_file_path, "w") as f:
                for partition in partitions:
                    f.write(f"{partition}\n")

            return partitions

    def generate_parallel(
        self, num_partitions: int, uniprot_txt_path: str
    ) -> List[int]:
        with open(uniprot_txt_path) as uniprot_file:
            reader = UniprotTextReader(uniprot_file)
            peptides_per_mass: Dict[int, int] = defaultdict(int)
            num_proteins = 0
            num_peptides = 0
            num_peptides_lock = threading.Lock()

            def process_protein(protein):
                nonlocal num_peptides, num_proteins
                local_peptides = 0

                for peptide_sequence in self.proteomics.digest(protein.sequence):
                    mass = self.proteomics.calculate_mass(peptide_sequence)
                    peptides_per_mass[mass] += 1
                    local_peptides += 1
                with num_peptides_lock:
                    num_proteins += 1
                    num_peptides += local_peptides

            with ThreadPoolExecutor() as executor:
                tasks = [
                    executor.submit(process_protein, protein) for protein in reader
                ]
                wait(tasks)

            logging.info("Number of proteins: %d", num_proteins)
            logging.info("Number of peptides: %d", num_peptides)
            logging.info("Partitions: %d", num_partitions)

            partitions = self._get_partitions(
                num_partitions, num_peptides, peptides_per_mass
            )

            peptide_counts = self._get_peptide_counts(
                num_partitions, partitions, peptides_per_mass
            )

            for i in range(num_partitions):
                logging.info("Partition %d: %d peptides", i, peptide_counts[i])

            out_file_path = "out/partitions.txt"
            os.makedirs(os.path.dirname(out_file_path), exist_ok=True)
            with open(out_file_path, "w") as f:
                for partition in partitions:
                    f.write(f"{partition}\n")

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
