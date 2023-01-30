import logging
import time
from macpep_scylladb.modules.Query import Query
from macpep_scylladb.proteomics.mass import to_int


class QueryPerformance:
    def __init__(self, query: Query):
        self.tolerance = 500000
        self.query = query

    def _get_tolerance_limits(self, mass):
        return mass - self.tolerance, mass + self.tolerance

    def query_mass_ranges(
        self, server: str, mass_file_path: str, partitions_file_path: str
    ):
        with open(mass_file_path) as f:
            mass_list = list(map(lambda x: to_int(float(x)), f.read().splitlines()))
        logging.info(f"Found {len(mass_list)} masses")

        total = 0
        start_time = time.time()

        for mass in mass_list:
            lower, upper = self._get_tolerance_limits(mass)
            total += len(
                self.query.peptides_by_mass_range(
                    server, lower, upper, partitions_file_path
                )
            )

        finish_time = time.time()
        seconds_elapsed = finish_time - start_time

        logging.info(f"Queried {total} peptides in {seconds_elapsed:.2f} seconds")
