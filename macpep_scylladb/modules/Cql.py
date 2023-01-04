import random
import string
from typing import List
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import connection
from cassandra.concurrent import execute_concurrent
from macpep_scylladb.database.Peptide import Peptide
from cassandra.cluster import Cluster

from macpep_scylladb.database.Protein import Protein

protein = "MDGPTRGHGLRKKRRSRSQRDRERRSRAGLGTGAAGGIGAGRTRAPSLASSSGSDKEDNGKPPSSAPSRPRPPRRKRRESTSAEEDIIDGFAMTSFVTFEALEKDVAVKPQERAEKRQTPLTKKKREALTNGLSFHSKKSRLSHSHHYSSDRENDRNLCQHLGKRKKMPKGLRQLKPGQNSCRDSDSESASGESKGFQRSSSRERLSDSSAPSSLGTGYFCDSDSDQEEKASDASSEKLFNTVLVNKDPELGVGALPEHNQDAGPIVPKISGLERSQEKSQDCCKEPVFEPVVLKDPHPQLPQLPSQAQAEPQLQIPSPGPDLVPRTEAPPQFPPPSTQPAQGPPEAQLQPAPLPQVQQRPPRPQSPSHLLQQTLPPVQSHPSSQSLSQPLSAYNSSSLSLNSLSSRSSTPAKTQPAPPHISHHPSASPFPLSLPNHSPLHSFTPTLQPPAHSHHPNMFAPPTALPPPPPLTSGSLQVPGHPAGSTYSEQDILRQELNTRFLASQSADRGASLGPPPYLRTEFHQHQHQHQHTHQHTHQHTFTPFPHAIPPTAIMPTPAPPMFDKYPTKVDPFYRHSLFHSYPPAVSGIPPMIPPTGPFGSLQGAFQPKTSNPIDVAARPGTVPHTLLQKDPRLTDPFRPMLRKPGKWCAMHVHIAWQIYHHQQKVKKQMQSDPHKLDFGLKPEFLSRPPGPSLFGAIHHPHDLARPSTLFSAAGAAHPTGTPFGPPPHHSNFLNPAAHLEPFNRPSTFTGLAAVGGNAFGGLGNPSVTPNSVFGHKDSPSVQNFSNPHEPWNRLHRTPPSFPTPPPWLKPGELERSASAAAHDRDRDVDKRDSSVSKDDKERESVEKRHPSHPSPAPPVPVSALGHNRSSTDPTTRGHLNTEAREKDKPKEKERDHSGSRKDLTTEEHKAKESHLPERDGHSHEGRAAGEEPKQLSRVPSPYVRTPGVDSTRPNSTSSREAEPRKGEPAYENPKKNAEVKVKEERKEDHDLPTEAPQAHRTSEAPPPSSSASASVHPGPLASMPMTVGVTGIHAMNSIGSLDRTRMVTPFMGLSPIPGGERFPYPSFHWDPMRDPLRDPYRDLDMHRRDPLGRDFLLRNDPLHRLSTPRLYEADRSFRDREPHDYSHHHHHHHHPLAVDPRREHERGGHLDERERLHVLREDYEHPRLHPVHPASLDGHLPHPSLLTPGLPSMHYPRISPTAGHQNGLLNKTPPTAALSAPPPLISTLGGRPGSPRRTTPLSAEIRERPPSHTLKDIEAR"


class Cql:
    def __init__(self):
        self.connected = False

    def _connect(self, server):
        connection.setup([server], "macpep")
        self.connected = True

    def setup(self, server: str):
        self.create_keyspace(server)
        self.create_tables(server)
        self.insert_test(server)

    def create_keyspace(self, server: str):
        cluster = Cluster([server])
        session = cluster.connect()

        keyspaces = session.execute("SELECT keyspace_name FROM system_schema.keyspaces")
        if "macpep" in [keyspace.keyspace_name for keyspace in keyspaces]:
            print("Keyspace 'macpep' already exists, skipping creation.")
        else:
            session.execute(
                """CREATE KEYSPACE macpep
                WITH REPLICATION = {'class': 'NetworkTopologyStrategy',
                'replication_factor': 1}"""
            )
        session.shutdown()
        cluster.shutdown()

    def create_tables(self, server: str):
        if not self.connected:
            self._connect(server)
        sync_table(Peptide)
        sync_table(Protein)

    def insert_protein(self, server: str, p: Protein):
        if not self.connected:
            self._connect(server)
        p.save()

    def insert_proteins(self, session, proteins: List[Protein]):
        insert_statement_str = """INSERT INTO macpep.proteins ("partition", "accession", "secondary_accessions", "entry_name", "name", "sequence", "taxonomy_id", "proteome_id", "is_reviewed", "updated_at") VALUES (?,?,?,?,?,?,?,?,?,?)"""
        insert_statement = session.prepare(insert_statement_str)

        statements_and_params = []
        for p in proteins:
            params = (
                p.partition,
                p.accession,
                p.secondary_accessions,
                p.entry_name,
                p.name,
                p.sequence,
                p.taxonomy_id,
                p.proteome_id,
                p.is_reviewed,
                p.updated_at,
            )
            statements_and_params.append((insert_statement, params))

        execute_concurrent(session, statements_and_params, raise_on_first_error=True)

    def upsert_peptides(self, session, peptides: List[Peptide]):
        # Using execute_concurrent with the same UPDATE statement that upsert_peptides uses under the hood is significantly faster
        update_statement_str = """UPDATE macpep.peptides SET "proteins" = "proteins" + ?, "length" = ?, "number_of_missed_cleavages" = ?, "a_count" = ?, "b_count" = ?, "c_count" = ?, "d_count" = ?, "e_count" = ?, "f_count" = ?, "g_count" = ?, "h_count" = ?, "i_count" = ?, "j_count" = ?, "k_count" = ?, "l_count" = ?, "m_count" = ?, "n_count" = ?, "o_count" = ?, "p_count" = ?, "q_count" = ?, "r_count" = ?, "s_count" = ?, "t_count" = ?, "u_count" = ?, "v_count" = ?, "w_count" = ?, "y_count" = ?, "z_count" = ?, "n_terminus" = ?, "c_terminus" = ?, "is_metadata_up_to_date" = ? WHERE "partition" = ? AND "mass" = ? AND "sequence" = ?"""
        update_statement = session.prepare(update_statement_str)

        statements_and_params = []
        for p in peptides:
            params = (
                p.proteins,
                p.length,
                p.number_of_missed_cleavages,
                p.a_count,
                p.b_count,
                p.c_count,
                p.d_count,
                p.e_count,
                p.f_count,
                p.g_count,
                p.h_count,
                p.i_count,
                p.j_count,
                p.k_count,
                p.l_count,
                p.m_count,
                p.n_count,
                p.o_count,
                p.p_count,
                p.q_count,
                p.r_count,
                p.s_count,
                p.t_count,
                p.u_count,
                p.v_count,
                p.w_count,
                p.y_count,
                p.z_count,
                p.n_terminus,
                p.c_terminus,
                p.is_metadata_up_to_date,
                p.partition,
                p.mass,
                p.sequence,
            )
            statements_and_params.append((update_statement, params))

        execute_concurrent(session, statements_and_params, raise_on_first_error=True)

    def upsert_peptide(self, server: str, p: Peptide):
        if not self.connected:
            self._connect(server)
        p.validate()
        # This seems to do it in one command, instead of SELECT + Create/Update
        Peptide.objects(
            partition=p.partition,
            mass=p.mass,
            sequence=p.sequence,
        ).update(
            proteins__add=p.proteins,
            length=p.length,
            number_of_missed_cleavages=p.number_of_missed_cleavages,
            a_count=p.a_count,
            b_count=p.b_count,
            c_count=p.c_count,
            d_count=p.d_count,
            e_count=p.e_count,
            f_count=p.f_count,
            g_count=p.g_count,
            h_count=p.h_count,
            i_count=p.i_count,
            j_count=p.j_count,
            k_count=p.k_count,
            l_count=p.l_count,
            m_count=p.m_count,
            n_count=p.n_count,
            o_count=p.o_count,
            p_count=p.p_count,
            q_count=p.q_count,
            r_count=p.r_count,
            s_count=p.s_count,
            t_count=p.t_count,
            u_count=p.u_count,
            v_count=p.v_count,
            w_count=p.w_count,
            y_count=p.y_count,
            z_count=p.z_count,
            n_terminus=p.n_terminus,
            c_terminus=p.c_terminus,
            is_metadata_up_to_date=p.is_metadata_up_to_date,
        )

    def insert_loop(self, server: str, elements: int):
        if not self.connected:
            self._connect(server)
        for _ in range(elements):
            partition = random.randint(0, 1000)
            mass = random.randint(0, 1000000000)
            sequence = "".join(random.choices(string.ascii_uppercase, k=10))
            Peptide(
                partition=partition, mass=mass, sequence=sequence, proteins={protein}
            ).save()
