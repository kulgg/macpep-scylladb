from typing import List, Set, Tuple

from macpep_scylladb.proteomics.AminoAcid import AminoAcid
from macpep_scylladb.proteomics.AminoAcid import X as UnknownAminoAcid
from macpep_scylladb.proteomics.digest import (
    differentiate_ambigous_sequences,
    is_sequence_containing_replaceable_ambigous_amino_acids,
)
from macpep_scylladb.proteomics.DigestEnzyme import DigestEnzyme
from macpep_scylladb.proteomics.NeutralLoss import H2O
from macpep_scylladb.proteomics.Trypsin import Trypsin


class Proteomics:
    def __init__(self):
        pass

    def calculate_mass(self, sequence: str) -> int:
        mass: int = H2O.mono_mass
        for c in sequence:
            mass += AminoAcid.get_by_one_letter_code(c).mono_mass
        return mass

    def digest(
        self,
        sequence: str,
        enzyme: DigestEnzyme = Trypsin(
            max_number_of_missed_cleavages=2,
            minimum_peptide_length=5,
            maximum_peptide_length=60,
        ),
    ) -> List[Tuple[str, int]]:
        peptides: Set[Tuple[str, int]] = set()
        protein_parts = enzyme.cleavage_regex.split(sequence)
        peptide_range = range(
            enzyme.minimum_peptide_length, enzyme.maximum_peptide_length + 1
        )

        for part_index in range(len(protein_parts)):
            last_part_to_add = min(
                part_index + enzyme.max_number_of_missed_cleavages + 1,
                len(protein_parts),
            )
            peptide_sequence = ""
            for missed_cleavage in range(part_index, last_part_to_add):
                peptide_sequence += protein_parts[missed_cleavage]
                if (
                    len(peptide_sequence) in peptide_range
                    and UnknownAminoAcid.one_letter_code not in peptide_sequence
                ):
                    peptides.add((peptide_sequence, missed_cleavage - part_index))
                    if is_sequence_containing_replaceable_ambigous_amino_acids(
                        peptide_sequence
                    ):
                        differentiated_sequences = differentiate_ambigous_sequences(
                            peptide_sequence
                        )
                        for sequence in differentiated_sequences:
                            peptides.add((sequence, missed_cleavage - part_index))
        return list(peptides)
