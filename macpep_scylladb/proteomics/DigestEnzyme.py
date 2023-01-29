import re

from attr import dataclass


@dataclass
class DigestEnzyme:
    name: str
    shortcut: str
    cleavage_regex: re.Pattern
    missed_cleavage_regex: re.Pattern
    max_number_of_missed_cleavages: int
    minimum_peptide_length: int
    maximum_peptide_length: int
