import logging
from cassandra.cluster import Cluster


class ProteinDigist:
    def __init__(self):
        self.port = 9042

    def setup(self):
        for i in range(3):
            cluster = Cluster(
                ["127.0.0.1"], port=(self.port + i), control_connection_timeout=10
            )
            session = cluster.connect(wait_for_all_pools=True)

            session.execute(
                """
                    CREATE KEYSPACE IF NOT EXISTS excalibur WITH replication = {
                        'class': 'NetworkTopologyStrategy',
                        'replication_factor' : 1
                    }
                """
            )

            session.execute("USE excalibur")

            session.execute(
                """
                    CREATE TABLE IF NOT EXISTS excalibur.proteins (
                        accession text,
                        entry_name text,
                        name text,
                        sequence text,
                        taxonomy_id int,
                        proteome_id text,
                        is_reviewed boolean,
                        PRIMARY KEY(sequence)
                    );
                """
            )

            session.execute(
                """
                    INSERT INTO
                        proteins(
                            accession,
                            entry_name,
                            name,
                            sequence,
                            taxonomy_id,
                            proteome_id,
                            is_reviewed
                        )
                        VALUES (
                            'accession',
                            'entry name',
                            'name',
                            'sequence',
                            123,
                            'proteome_id',
                            True
                        );
                """
            )

    def digist(self):
        for i in range(3):
            cluster = Cluster(
                ["127.0.0.1"], port=(9042 + i), control_connection_timeout=10
            )
            session = cluster.connect(wait_for_all_pools=True)
            session.execute("USE excalibur")
            rows = session.execute("SELECT * FROM proteins")

            for row in rows:
                logging.info("%s %s %s", row.accession, row.name, row.sequence)
