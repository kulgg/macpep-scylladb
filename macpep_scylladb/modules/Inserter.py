from collections import Counter
import csv
import logging
import time
from progress.bar import Bar
import multiprocessing
import threading
from time import sleep
from cassandra.cluster import Cluster
from cassandra.cluster import Session
from macpep_scylladb.database.Peptide import Peptide
from macpep_scylladb.models.Protein import Protein
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

    def _process_peptides(self, protein: Protein, session: Session = None):
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
                is_swiss_prot=protein.is_reviewed,
                taxonomy_ids={protein.taxonomy_id},
                unique_taxonomy_ids={},
                proteome_ids={protein.proteome_id},
            )
            if not session:
                self.cql.upsert_peptide(self.server, peptide)
                self.num_processed_peptides += 1
            else:
                peptides.append(peptide)
        if session:
            self.cql.upsert_peptides(session, peptides)
            with self.lock:
                self.num_processed_peptides += len(peptides)

    def _worker(self, queue):
        cluster = Cluster([self.server])
        session = cluster.connect("macpep")

        while True:
            protein = queue.get()
            if not protein:
                cluster.shutdown()
                break
            self._process_peptides(protein, session)

    def _progress_worker(self, queue):
        old_num_processed = 0
        start_time = time.time()
        while not self.stopped:
            qsize = queue.qsize()
            num_processed = self.num_proteins_added_to_queue - qsize
            elapsed_time = time.time() - start_time
            items_per_second = num_processed / elapsed_time
            self.bar.suffix = (
                f"{num_processed}/{self.num_total_proteins} Proteins"
                f" {items_per_second:.2f}P/sec {self.num_processed_peptides} Peptides"
            )
            self.bar.next(num_processed - old_num_processed)
            old_num_processed = num_processed
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

            while not self.stopped:
                if i == T:
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
                i += 1
                sleep(1)

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

        self.num_proteins_added_to_queue = 0
        self.num_processed_peptides = 0

        start_time = time.time()
        for protein in reader:
            self.num_proteins_added_to_queue += 1
            protein_db = to_database(protein)
            self.cql.insert_protein(server, protein_db)
            self._process_peptides(protein)
            elapsed_time = time.time() - start_time
            items_per_second = self.num_proteins_added_to_queue / elapsed_time
            bar.suffix = (
                f"{self.num_proteins_added_to_queue}/{num_lines} {items_per_second:.2f} proteins/sec"
            )
            bar.next()

        logging.info("Number of proteins: %d", self.num_proteins_added_to_queue)
        logging.info("Number of peptides: %d", self.num_processed_peptides)

        uniprot_f.close()

    def run_multi(
        self,
        server: str,
        partitions_file_path: str,
        uniprot_file_path: str,
        num_threads: int = 14,
        performance_log_interval: int = 60,
    ):
        self.server = server
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
        queue = m.Queue()
        num_worker_threads = num_threads
        self.lock = threading.Lock()
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

        performance_logger = threading.Thread(
            target=self._performance_logger,
            args=(
                queue,
                performance_log_interval,
            ),
        )
        performance_logger.start()

        for protein in reader:
            self.num_proteins_added_to_queue += 1
            self.cql.insert_protein(self.server, to_database(protein))
            queue.put(protein)

        for _ in range(1000):
            queue.put(None)

        for thread in threads:
            thread.join()

        self.stopped = True
        progress_logger.join()
        performance_logger.join()

        logging.info("Number of proteins: %d", self.num_proteins_added_to_queue)
        logging.info("Number of peptides: %d", self.num_processed_peptides)

        uniprot_f.close()
