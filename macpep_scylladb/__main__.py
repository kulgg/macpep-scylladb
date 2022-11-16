import logging
import sys

import fire
from exitstatus import ExitStatus
from macpep_scylladb.modules.CqlTest import CqlTest
from macpep_scylladb.modules.protein_digist.ProteinDigist import ProteinDigist
from macpep_scylladb.modules.UniprotDigest import UniprotDigest


class Commands:
    def __init__(self):
        self.digest = UniprotDigest()
        self.cql = CqlTest()
        self.pro_digist = ProteinDigist


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
