from macpep_scylladb.models.AminoAcid import AminoAcid
from macpep_scylladb.models.NeutralLoss import H2O


class Proteomics:
    def __init__(self):
        pass

    def calculate_mass(self, sequence: str) -> int:
        mass: int = H2O.mono_mass
        for c in sequence:
            mass += AminoAcid.get_by_one_letter_code(c).mono_mass
        return mass
