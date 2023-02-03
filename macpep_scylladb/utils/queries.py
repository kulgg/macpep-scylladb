from cassandra.concurrent import execute_concurrent


def prepare_peptide_query(session):
    query_str = """SELECT * FROM macpep.peptides WHERE "partition" = ? AND "mass" >= ? AND "mass" <= ?"""
    query_statement = session.prepare(query_str)
    return query_statement


def query_peptides(session, statement, partition, lower_mass, upper_mass):
    params = (partition, lower_mass, upper_mass)
    return session.execute(statement, params)


def query_peptides_list(session, statement, params_list):
    statements_and_params = []
    for p in params_list:
        statements_and_params.append((statement, p))

    return execute_concurrent(session, statements_and_params, raise_on_first_error=True)


# def query_peptides_with_callback(
#     session: Session,
#     partition: int,
#     lower_mass: int,
#     upper_mass: int,
#     result_cb,
#     error_cb,
# ):
#     query_str = (
#         "SELECT * FROM macpep.peptides WHERE partition = {partition} AND mass >="
#         " {lower} AND mass <= {upper}"
#     )
#     # query_statement = session.prepare(query_str)

#     # params = (partition, lower_mass, upper_mass)
#     query = query_str.format(partition=partition, lower=lower_mass, upper=upper_mass)
#     future = session.execute_async(query=query)
#     future.add_callbacks(result_cb, error_cb)

#     return future

# def query_peptides()
