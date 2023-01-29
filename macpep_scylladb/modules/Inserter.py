from collections import Counter, defaultdict
import csv
import logging
import random
import time
from typing import List
from progress.bar import Bar
import multiprocessing
import threading
from time import sleep
from multiprocessing import Process, Value
from cassandra.cluster import Cluster
from macpep_scylladb.database.Peptide import Peptide
from macpep_scylladb.models.Protein import Protein
from macpep_scylladb.modules.Partitioner import Partitioner
from macpep_scylladb.modules.Proteomics import Proteomics
from macpep_scylladb.utils.UniprotTextReader import UniprotTextReader
from macpep_scylladb.utils.dml import (
    GeniusRetryPolicy,
    batch_upsert_peptides,
    insert_proteins,
    upsert_peptides,
)
from cassandra.policies import DCAwareRoundRobinPolicy


class Inserter:
    def __init__(self, partitioner: Partitioner, proteomics: Proteomics):
        self.partitioner = partitioner
        self.proteomics = proteomics
        self.stopped = False

    def _process_peptides(self, protein: Protein):
        peptides = []

        for peptide_sequence, num_of_missed_cleavages in self.proteomics.digest(
            protein.sequence
        ):
            # any(review_statuses),
            # # is_trembl when not all are true
            # not all(review_statuses),
            mass = self.proteomics.calculate_mass(peptide_sequence)
            partition = self.partitioner.get_partition_index(self.partitions, mass)
            amino_acid_counter = Counter(peptide_sequence)
            peptide = Peptide(
                partition=partition,
                mass=mass,
                sequence=peptide_sequence,
                proteins={protein.accession},
                length=len(peptide_sequence),
                number_of_missed_cleavages=num_of_missed_cleavages,
                a_count=amino_acid_counter["A"],
                b_count=amino_acid_counter["B"],
                c_count=amino_acid_counter["C"],
                d_count=amino_acid_counter["D"],
                e_count=amino_acid_counter["E"],
                f_count=amino_acid_counter["F"],
                g_count=amino_acid_counter["G"],
                h_count=amino_acid_counter["H"],
                i_count=amino_acid_counter["I"],
                j_count=amino_acid_counter["J"],
                k_count=amino_acid_counter["K"],
                l_count=amino_acid_counter["L"],
                m_count=amino_acid_counter["M"],
                n_count=amino_acid_counter["N"],
                o_count=amino_acid_counter["O"],
                p_count=amino_acid_counter["P"],
                q_count=amino_acid_counter["Q"],
                r_count=amino_acid_counter["R"],
                s_count=amino_acid_counter["S"],
                t_count=amino_acid_counter["T"],
                u_count=amino_acid_counter["U"],
                v_count=amino_acid_counter["V"],
                w_count=amino_acid_counter["W"],
                y_count=amino_acid_counter["Y"],
                z_count=amino_acid_counter["Z"],
                n_terminus=ord(peptide_sequence[0]),
                c_terminus=ord(peptide_sequence[-1]),
                # is_swiss_prot=protein.is_reviewed,
                # taxonomy_ids={protein.taxonomy_id},
                # unique_taxonomy_ids={},
                # proteome_ids={protein.proteome_id},
            )
            peptides.append(peptide)
        return peptides

    def _upsert_peptides(self, session, peptide_list, num_peptides_processed):
        upsert_peptides(session, peptide_list)
        # peptides = defaultdict(list)
        # for p in peptide_list:
        #     peptides[p.partition].append(p)
        # for ps in peptides.values():
        #     batch_upsert_peptides(session, ps)
        num_peptides_processed.value += len(peptide_list)

    def _worker(self, protein_queue, threshold, num_peptides_processed, timeout):
        cluster = Cluster(self.server)
        session = cluster.connect("macpep")
        session.default_timeout = 30

        peptide_list = []

        while True:
            protein = protein_queue.get()
            if not protein:
                break
            peptide_list.extend(self._process_peptides(protein))

            if len(peptide_list) > threshold:
                self._upsert_peptides(session, peptide_list, num_peptides_processed)
                peptide_list = []
            sleep(timeout)

        self._upsert_peptides(session, peptide_list)
        cluster.shutdown()

    def _progress_worker(self, queue, num_peptides_processed):
        old_num_proteins_processed = 0
        start_time = time.time()
        while not self.stopped:
            qsize = queue.qsize()
            num_proteins_processed = self.num_proteins_added_to_queue - qsize
            elapsed_time = time.time() - start_time
            proteins_per_second = num_proteins_processed / elapsed_time
            peptides_per_second = num_peptides_processed.value / elapsed_time
            self.bar.suffix = (
                f"{num_proteins_processed}/{self.num_total_proteins} Proteins"
                f" {proteins_per_second:.0f}P/sec"
                f" {peptides_per_second:.0f}Pep/sec"
                f" {num_peptides_processed.value} Peptides"
            )
            self.bar.next(num_proteins_processed - old_num_proteins_processed)
            old_num_proteins_processed = num_proteins_processed
            sleep(0.1)

    def _performance_logger(self, queue, T):
        with open("data/insertion_performance.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    "seconds",
                    "processed_proteins",
                    "processed_peptides",
                    "proteins/sec",
                    "peptides/sec",
                ]
            )

            start_time = time.time()
            prev_time = time.time()
            prev_num_processed_proteins = 0
            prev_num_processed_peptides = 0
            i = 0

            while True:
                if i == T or self.stopped:
                    now = time.time()
                    elapsed_secs = int(now - prev_time)
                    qsize = queue.qsize()
                    num_processed_proteins = self.num_proteins_added_to_queue - qsize
                    proteins_per_sec = (
                        num_processed_proteins - prev_num_processed_proteins
                    ) / elapsed_secs
                    peptides_per_sec = (
                        self.num_processed_peptides - prev_num_processed_peptides
                    ) / elapsed_secs

                    writer.writerow(
                        [
                            int(now - start_time),
                            num_processed_proteins,
                            self.num_processed_peptides,
                            proteins_per_sec,
                            peptides_per_sec,
                        ]
                    )
                    prev_time = now
                    prev_num_processed_proteins = num_processed_proteins
                    prev_num_processed_peptides = self.num_processed_peptides
                    i = 0

                    if self.stopped:
                        break
                i += 1
                sleep(1)

    def run_multi(
        self,
        server: str,
        partitions_file_path: str,
        uniprot_file_path: str,
        num_worker_processes: int = 14,
        performance_log_interval: int = 60,
        num_insert_threshold: int = 10000,
        max_protein_queue_size: int = 2000,
        timeout: float = 0.0,
    ):
        self.server = server.split(",")
        partitions_file = open(partitions_file_path, "r")
        self.partitions = list(map(int, partitions_file.read().splitlines()))
        partitions_file.close()
        uniprot_f = open(uniprot_file_path, "r")
        self.num_total_proteins = sum(
            1 for line in open(uniprot_file_path) if line.startswith("//")
        )
        self.bar = Bar("Processing", max=self.num_total_proteins)
        logging.info("Total proteins: %d", self.num_total_proteins)
        reader = UniprotTextReader(uniprot_f)

        self.num_proteins_added_to_queue = 0
        self.num_processed_peptides = 0

        m = multiprocessing.Manager()
        protein_queue = m.Queue()
        worker_processes = []
        num_peptides_processed = Value("i", 0)

        for _ in range(num_worker_processes):
            p = Process(
                target=self._worker,
                args=(
                    protein_queue,
                    num_insert_threshold,
                    num_peptides_processed,
                    timeout,
                ),
            )
            p.start()
            worker_processes.append(p)

        progress_logger = threading.Thread(
            target=self._progress_worker,
            args=(
                protein_queue,
                num_peptides_processed,
            ),
        )
        progress_logger.start()

        performance_logger = threading.Thread(
            target=self._performance_logger,
            args=(
                protein_queue,
                performance_log_interval,
            ),
        )
        performance_logger.start()

        protein_list = []
        cluster = Cluster(self.server)
        session = cluster.connect("macpep")

        for protein in reader:
            if protein_queue.qsize() > max_protein_queue_size:
                sleep(0.1)
                continue
            self.num_proteins_added_to_queue += 1
            protein_list.append(protein)
            protein_queue.put(protein)
            if len(protein_list) > 500:
                insert_proteins(session, protein_list)
                protein_list = []

        insert_proteins(session, protein_list)

        for _ in range(1000):
            protein_queue.put(None)

        for thread in worker_processes:
            thread.join()

        self.stopped = True
        progress_logger.join()
        performance_logger.join()

        logging.info("Number of proteins: %d", self.num_proteins_added_to_queue)
        logging.info("Number of peptides: %d", num_peptides_processed)

        uniprot_f.close()

    def a(self, list: List[str]):
        logging.info(list)
        logging.info(type(list).__name__)
