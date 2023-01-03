from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Protein(Model):
    accession = columns.Text(primary_key=True, required=True)
    secondary_accessions = columns.List(columns.Text, required=True)
    entry_name = columns.Text(required=True)
    name = columns.Text()
    sequence = columns.Text(required=True)
    taxonomy_id = columns.Integer()
    proteome_id = columns.Text()
    is_reviewed = columns.Boolean(required=True)
    updated_at = columns.BigInt(default=0, required=True)
