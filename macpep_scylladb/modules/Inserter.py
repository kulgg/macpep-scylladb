import logging
import time
from progress.bar import Bar
import multiprocessing
import threading
from time import sleep
from macpep_scylladb.database.Peptide import Peptide
from macpep_scylladb.modules.Cql import Cql
from macpep_scylladb.modules.Partitioner import Partitioner
from macpep_scylladb.modules.Proteomics import Proteomics
from macpep_scylladb.utils.UniprotTextReader import UniprotTextReader
from macpep_scylladb.utils.model_convert import to_database


class Inserter:
    def __init__(self, partitioner: Partitioner, proteomics: Proteomics, cql: Cql):
        self.partitioner = partitioner
        self.proteomics = proteomics
        self.cql = cql
        self.stopped = False

    def _process_peptides(self, protein, cql=None):
        if not cql:
            cql = self.cql
        for peptide_sequence in self.proteomics.digest(protein.sequence):
            mass = self.proteomics.calculate_mass(peptide_sequence)
            partition = self.partitioner.get_partition_index(self.partitions, mass)
            peptide = Peptide(
                partition=partition,
                mass=mass,
                sequence=peptide_sequence,
                proteins={protein.sequence},
                length=len(peptide_sequence),
                number_of_missed_cleavages=0,
                n_terminus=0,
                c_terminus=0,
            )
            cql.upsert_peptide(self.server, peptide)
            # num_peptides += 1
            # if num_peptides % 100000 == 0:
            #     logging.info("Processed %d peptides", num_peptides)

    def _worker(self, queue):
        cql = Cql()
        while True:
            protein = queue.get()
            if protein is None:
                break
            self._process_peptides(protein, cql)

    def _progress_worker(self, queue):
        old_num_processed = 0
        start_time = time.time()
        while not self.stopped:
            qsize = queue.qsize()
            num_processed = self.num_proteins - qsize
            elapsed_time = time.time() - start_time
            items_per_second = num_processed / elapsed_time
            self.bar.suffix = (
                f"{num_processed}/{self.num_lines} {items_per_second:.2f} proteins/sec"
            )
            self.bar.next(num_processed - old_num_processed)
            old_num_processed = num_processed
            # logging.info(
            #     "Queue size %d Processed %d\nProgress %.2f%%",
            #     qsize,
            #     num_processed,
            #     num_processed / self.num_lines,
            # )
            sleep(0.1)

    def run_serial(
        self, server: str, partitions_file_path: str, uniprot_file_path: str
    ):
        self.server = server
        partitions_file = open(partitions_file_path, "r")
        self.partitions = list(map(int, partitions_file.read().splitlines()))
        partitions_file.close()
        num_lines = sum(1 for line in open(uniprot_file_path) if line.startswith("//"))
        bar = Bar("Processing", max=num_lines)
        uniprot_f = open(uniprot_file_path, "r")
        reader = UniprotTextReader(uniprot_f)

        num_proteins = 0
        num_peptides = 0

        start_time = time.time()
        for protein in reader:
            num_proteins += 1
            protein_db = to_database(protein)
            self.cql.insert_protein(server, protein_db)
            self._process_peptides(protein)
            elapsed_time = time.time() - start_time
            items_per_second = num_proteins / elapsed_time
            bar.suffix = (
                f"{num_proteins}/{num_lines} {items_per_second:.2f} proteins/sec"
            )
            bar.next()

        logging.info("Number of proteins: %d", num_proteins)
        logging.info("Number of peptides: %d", num_peptides)

        uniprot_f.close()

    def run_multi(self, server: str, partitions_file_path: str, uniprot_file_path: str):
        self.server = server
        partitions_file = open(partitions_file_path, "r")
        self.partitions = list(map(int, partitions_file.read().splitlines()))
        partitions_file.close()
        uniprot_f = open(uniprot_file_path, "r")
        self.num_lines = sum(
            1 for line in open(uniprot_file_path) if line.startswith("//")
        )
        self.bar = Bar("Processing", max=self.num_lines)
        logging.info("Total proteins: %d", self.num_lines)
        reader = UniprotTextReader(uniprot_f)

        self.num_proteins = 0
        num_peptides = 0

        m = multiprocessing.Manager()
        queue = m.Queue()
        num_worker_threads = 10
        threads = []
        for _ in range(num_worker_threads):
            t = threading.Thread(target=self._worker, args=(queue,))
            t.start()
            threads.append(t)

        progress_logger = threading.Thread(
            target=self._progress_worker,
            args=(queue,),
        )
        progress_logger.start()

        for protein in reader:
            self.num_proteins += 1
            protein_db = to_database(protein)
            self.cql.insert_protein(server, protein_db)
            queue.put(protein)

        for _ in range(num_worker_threads):
            queue.put(None)

        for thread in threads:
            thread.join()

        self.stopped = True
        progress_logger.join()

        logging.info("Number of proteins: %d", self.num_proteins)
        logging.info("Number of peptides: %d", num_peptides)

        uniprot_f.close()
