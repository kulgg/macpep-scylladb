import logging
import sys

import fire
from exitstatus import ExitStatus
from macpep_scylladb.modules.CqlTest import CqlTest
from macpep_scylladb.modules.Partitioner import Partitioner
from macpep_scylladb.modules.Proteomics import Proteomics


class Commands:
    def __init__(self):
        self.cql = CqlTest()
        self.proteomics = Proteomics()
        self.partitioner = Partitioner(self.proteomics)


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
