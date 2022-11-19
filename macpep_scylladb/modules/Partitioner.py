from typing import List
from macpep_scylladb.modules.Proteomics import Proteomics

from macpep_scylladb.utils.UniprotTextReader import UniprotTextReader


class Partitioner:
    def __init__(self, proteomics: Proteomics):
        self.proteomics = proteomics

    def generate_distribution(self, num_partitions: int, file_path: str) -> List[int]:
        with open(file_path) as uniprot_file:
            reader = UniprotTextReader(uniprot_file)

            for protein in reader:
                print(self.proteomics.calculate_mass(protein.sequence))
