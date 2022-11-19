from dataclasses import dataclass
from typing import List


@dataclass
class Protein:
    accession: str
    secondary_accessions: List[str]
    entry_name: str
    name: str
    sequence: str
    taxonomy_id: int
    proteome_id: str
    is_reviewed: bool
    updated_at: int
