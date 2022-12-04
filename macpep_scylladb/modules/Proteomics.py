from typing import List, Set
from macpep_scylladb.models.AminoAcid import (
    AminoAcid,
)
from macpep_scylladb.models.DigestEnzyme import DigestEnzyme
from macpep_scylladb.models.NeutralLoss import H2O
from macpep_scylladb.models.Trypsin import Trypsin

from macpep_scylladb.models.AminoAcid import X as UnknownAminoAcid
from macpep_scylladb.utils.proteomics.digest import (
    differentiate_ambigous_sequences,
    is_sequence_containing_replaceable_ambigous_amino_acids,
)


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
            max_number_of_missed_cleavages=3,
            minimum_peptide_length=3,
            maximum_peptide_length=60,
        ),
    ) -> List[str]:
        peptides: Set[str] = set()
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
                    peptides.add(
                        peptide_sequence
                        # peptide_mod.Peptide(
                        #     peptide_sequence, missed_cleavage - part_index
                        # )
                    )
                    if is_sequence_containing_replaceable_ambigous_amino_acids(
                        peptide_sequence
                    ):
                        differentiated_sequences = differentiate_ambigous_sequences(
                            peptide_sequence
                        )
                        for sequence in differentiated_sequences:
                            peptides.add(sequence)
        return list(peptides)
