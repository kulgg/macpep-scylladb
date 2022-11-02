import logging
from cassandra.cluster import Cluster


class CqlTest:
    def __init__(self):
        pass

    def setup(self):
        cluster = Cluster(["127.0.0.1"], port=9042, control_connection_timeout=10)
        session = cluster.connect(wait_for_all_pools=True)
        session.execute(
            """CREATE KEYSPACE excalibur
    WITH replication = {'class': 'NetworkTopologyStrategy', 'replication_factor' : 1}"""
        )
        session.execute("USE excalibur")
        session.execute(
            """CREATE TABLE excalibur.users (
 username text,
 name text,
 age int,
 PRIMARY KEY(username)
);"""
        )
        session.execute(
            "INSERT INTO users(username,name,age) VALUES ('aali24','Ali Amin',34);"
        )
        session.execute(
            "INSERT INTO users(username,name,age) VALUES ('jack01','Jack David',23);"
        )
        session.execute(
            "INSERT INTO users(username,name,age) VALUES ('ninopk','Nina Rehman',34);"
        )

    def query(self):
        cluster = Cluster(["127.0.0.1"], port=9042, control_connection_timeout=10)
        session = cluster.connect(wait_for_all_pools=True)
        session.execute("USE excalibur")
        rows = session.execute("SELECT * FROM users")
        for row in rows:
            logging.info("%d %s %s", row.age, row.name, row.username)
