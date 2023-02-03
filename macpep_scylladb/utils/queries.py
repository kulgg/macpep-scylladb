from cassandra.cluster import Session


def query_peptides(session: Session, partition: int, lower_mass: int, upper_mass: int):
    query_str = """SELECT * FROM macpep.peptides WHERE "partition" = ? AND "mass" >= ? AND "mass" <= ?"""
    query_statement = session.prepare(query_str)

    params = (partition, lower_mass, upper_mass)
    future = session.execute_async(query_statement, params)

    return future
