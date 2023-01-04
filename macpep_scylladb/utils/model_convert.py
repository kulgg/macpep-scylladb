from macpep_scylladb.database.Protein import Protein
from macpep_scylladb.models.Protein import Protein as ProteinModel
from macpep_scylladb.utils.hash import hash_string


def to_database(protein: ProteinModel) -> Protein:
    return Protein(
        partition=hash_string(protein.accession, 100),
        accession=protein.accession,
        secondary_accessions=protein.secondary_accessions,
        entry_name=protein.entry_name,
        name=protein.name,
        sequence=protein.sequence,
        taxonomy_id=protein.taxonomy_id,
        proteome_id=protein.proteome_id,
        is_reviewed=protein.is_reviewed,
        updated_at=protein.updated_at,
    )
