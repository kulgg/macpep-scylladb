import logging
import sys

import fire
from exitstatus import ExitStatus

from macpep_scylladb.modules.Cql import Cql
from macpep_scylladb.modules.Inserter import Inserter
from macpep_scylladb.modules.Partitioner import Partitioner
from macpep_scylladb.modules.Plots import Plots
from macpep_scylladb.modules.Proteomics import Proteomics
from macpep_scylladb.modules.Query import Query
from macpep_scylladb.modules.QueryPerformance import QueryPerformance


class Commands:
    def __init__(self):
        self.proteomics = Proteomics()
        self.partitioner = Partitioner(self.proteomics)
        self.cql = Cql()
        self.query = Query(self.proteomics, self.partitioner)
        self.inserter = Inserter(self.partitioner, self.proteomics)
        self.plots = Plots()
        self.qp = QueryPerformance(self.proteomics, self.partitioner)


def configure_logging():
    log_format = "%(asctime)s [%(levelname)s] %(module)s.%(funcName)s(): %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format)


def main():
    configure_logging()

    try:
        fire.Fire(Commands)
    except Exception as exception:
        logging.exception(exception)
        sys.exit(ExitStatus.failure)


if __name__ == "__main__":
    main()
