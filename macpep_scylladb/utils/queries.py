from cassandra.cluster import Session


def query_peptides_with_callback(
    session: Session,
    partition: int,
    lower_mass: int,
    upper_mass: int,
    result_cb,
    error_cb,
):
    query_str = (
        'SELECT * FROM macpep.peptides WHERE "partition" = {partition} AND "mass" >='
        ' {lower} AND "mass" <= {upper}'
    )
    # query_statement = session.prepare(query_str)

    # params = (partition, lower_mass, upper_mass)
    future = session.execute_async(
        query_str.format(partition=partition, lower=lower_mass, upper=upper_mass)
    )

    future.add_callbacks(result_cb, error_cb)
