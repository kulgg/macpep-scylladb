import logging
import concurrent.futures
import math
import timeit
from typing import List
from macpep_scylladb.modules.Partitioner import Partitioner
from macpep_scylladb.modules.Proteomics import Proteomics
from macpep_scylladb.modules.Query import Query
from macpep_scylladb.proteomics.mass import to_int


class QueryPerformance:
    def __init__(self, proteomics: Proteomics, partitioner: Partitioner):
        self.proteomics = proteomics
        self.partitioner = partitioner

    def _slice_list(self, a_list, chunk_size):
        for i in range(0, len(a_list), chunk_size):
            yield a_list[i : i + chunk_size]

    def _get_tolerance_limits(self, mass):
        tolerance = (mass / 1000000) * 5.0
        return to_int(mass - tolerance), to_int(mass + tolerance)

    def _query(
        self, servers: List[str], partitions_file_path: str, mass_list: List[int]
    ):
        query = Query(self.proteomics, self.partitioner)
        total = 0
        i = 0
        num_masses = len(mass_list)
        threshold = int(num_masses / 10)
        for mass in mass_list:
            if i % threshold == 0:
                logging.info(f"{i}/{num_masses}")
            lower, upper = self._get_tolerance_limits(mass)
            total += query.peptides_by_mass_range(
                servers, lower, upper, partitions_file_path
            )
            i += 1
        return total

    def _query_multithreaded(
        self,
        servers: List[str],
        partitions_file_path: str,
        mass_list: List[int],
        num_threads: int,
    ):
        total = 0
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=num_threads
        ) as executor:
            query_futures: List[concurrent.futures.Future] = [
                executor.submit(self._query, servers, partitions_file_path, m_slice)
                for m_slice in self._slice_list(
                    mass_list, math.ceil(len(mass_list) / num_threads)
                )
            ]
            for future in concurrent.futures.as_completed(query_futures):
                total += future.result()
        logging.info("Queried %d peptides total" % total)

    def query_mass_ranges(
        self,
        servers: str,
        mass_file_path: str,
        partitions_file_path: str,
        use_singlethreading: bool = True,
        use_multithreading: bool = True,
        num_threads: int = 16,
    ):
        servers = servers.split(",")
        with open(mass_file_path) as f:
            mass_list = list(map(lambda x: float(x), f.read().splitlines()))
        logging.info(f"Found {len(mass_list)} masses")

        if use_singlethreading:
            elapsed = timeit.timeit(
                lambda: logging.info(
                    "Queried"
                    f" {self._query(servers, partitions_file_path, mass_list)} peptides"
                ),
                number=1,
            )
            logging.info(f"Singlethreading time: {elapsed}")

        if use_multithreading:
            elapsed = timeit.timeit(
                lambda: self._query_multithreaded(
                    servers, partitions_file_path, mass_list, num_threads
                ),
                number=1,
            )
            logging.info(f"Multithreading time: {elapsed}")
