import re

from attr import dataclass

from macpep_scylladb.models.DigestEnzyme import DigestEnzyme


@dataclass
class Trypsin(DigestEnzyme):
    name: str = "Trypsin"
    shortcut: str = "try"
    cleavage_regex: re.Pattern = re.compile(r"(?<=[KR])(?!P)")
    missed_cleavage_regex: re.Pattern = re.compile(r"(R|K)(?!($|P))")
    max_number_of_missed_cleavages: int = 0
    minimum_peptide_length: int = 0
    maximum_peptide_length: int = 1
