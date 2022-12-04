import logging
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import connection
from macpep_scylladb.database.Peptide import Peptide
from cassandra.cluster import Cluster

from macpep_scylladb.modules.Proteomics import Proteomics
from macpep_scylladb.modules.Partitioner import Partitioner


class Cql:
    def __init__(self, proteomics: Proteomics, partitioner: Partitioner):
        self.proteomics = proteomics
        self.partitioner = partitioner
        self.partitions = [
            0,
            589307140804,
            945474040024,
            1612755360019,
            1614738647319,
            2529289540729,
            2947478329205,
            3018410767455,
            3684549317922,
            3841096254963,
        ]

    def create_keyspace(self, server: str):
        cluster = Cluster([server])
        session = cluster.connect()

        keyspaces = session.execute("SELECT keyspace_name FROM system_schema.keyspaces")
        if "macpep" in [keyspace.keyspace_name for keyspace in keyspaces]:
            print("Keyspace 'macpep' already exists, skipping creation.")
        else:
            session.execute(
                """CREATE KEYSPACE macpep
                WITH REPLICATION = {'class': 'SimpleStrategy',
                'replication_factor': 1}"""
            )
        session.shutdown()
        cluster.shutdown()

    def create_table(self, server: str):
        connection.setup([server], "macpep")
        sync_table(Peptide)

    def insert_test(self, server: str):
        connection.setup([server], "macpep")
        Peptide(partition=0, mass=502286345739, sequence="QLSR").save()
        Peptide(partition=2, mass=945474040024, sequence="SQRDRER").save()
        Peptide(
            partition=8,
            mass=3684549317922,
            sequence="ERLSDSSAPSSLGTGYFCDSDSDQEEKASDASSEK",
        ).save()
        Peptide(
            partition=5, mass=2529289540729, sequence="AGLGTGAAGGIGAGRTRAPSLASSSGSDK"
        ).save()
        Peptide(
            partition=6, mass=2947478329205, sequence="ISGLERSQEKSQDCCKEPVFEPVVLK"
        ).save()
        Peptide(
            partition=7, mass=3018410767455, sequence="DREPHDYSHHHHHHHHPLAVDPRR"
        ).save()
        Peptide(
            partition=9,
            mass=3841096254963,
            sequence="ISPTAGHQNGLLNKTPPTAALSAPPPLISTLGGRPGSPR",
        ).save()
        Peptide(partition=4, mass=1614738647319, sequence="EDHDLPTEAPQAHR").save()
        Peptide(partition=3, mass=1612755360019, sequence="SASAAAHDRDRDVDK").save()
        Peptide(partition=1, mass=589307140804, sequence="SSTPAK").save()

    def query_peptides_by_sequence(self, server, sequence: str):
        connection.setup([server], "macpep")
        mass = self.proteomics.calculate_mass(sequence)
        logging.info("Mass %d", mass)
        partition = self.partitioner.get_partition_index(self.partitions, mass)
        logging.info("Partition %d", partition)
        peptides = Peptide.objects.filter(
            partition=partition, mass=mass, sequence=sequence
        )
        logging.info(f"Found {peptides.count()} peptides with sequence {sequence}.")

        for peptide in peptides:
            print(peptide.sequence)

    def query_peptides_by_mass(self, server: str, mass: int):
        connection.setup([server], "macpep")
        logging.info("Mass %d", mass)
        partition = self.partitioner.get_partition_index(self.partitions, mass)
        logging.info("Partition %d", partition)
        peptides = Peptide.objects.filter(partition=partition, mass=mass)
        logging.info(f"Found {peptides.count()} peptides with mass {mass}.")

        for peptide in peptides:
            print(peptide.sequence)
