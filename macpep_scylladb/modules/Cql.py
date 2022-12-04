from cassandra.cqlengine.management import sync_table, create_keyspace_simple
from cassandra.cqlengine import connection
from macpep_scylladb.database.Peptide import Peptide
from cassandra.cluster import Cluster


class Cql:
    def __init__(self):
        pass

    def create_keyspace(self, server: str):
        cluster = Cluster([server])
        session = cluster.connect()

        keyspaces = session.execute("SELECT keyspace_name FROM system_schema.keyspaces")
        if "macpep" in [keyspace.keyspace_name for keyspace in keyspaces]:
            print("Keyspace 'macpep' already exists, skipping creation.")
        else:
            session.execute(
                "CREATE KEYSPACE macpep WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1}"
            )
        session.shutdown()
        cluster.shutdown()

    def create_table(self, server: str):
        connection.setup([server], "macpep")
        sync_table(Peptide)
