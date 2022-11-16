class Protein:
    def __init__(
        self,
        accession: str,
        # secondary_accessions: list,
        entry_name: str,
        name: str,
        sequence: str,
        taxonomy_id: int,
        proteome_id: str,
        is_reviewed: bool,
        # updated_at: int,
    ):
        self.accession = accession
        # self.secondary_accessions = secondary_accessions
        self.entry_name = entry_name
        self.name = name
        self.sequence = sequence
        self.taxonomy_id = taxonomy_id
        self.proteome_id = proteome_id
        self.is_reviewed = is_reviewed
        # self.updated_at = updated_at
