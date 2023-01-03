import logging
import random
import string
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import connection
from macpep_scylladb.database.Peptide import Peptide
from cassandra.cluster import Cluster

from macpep_scylladb.database.Protein import Protein

protein = "MDGPTRGHGLRKKRRSRSQRDRERRSRAGLGTGAAGGIGAGRTRAPSLASSSGSDKEDNGKPPSSAPSRPRPPRRKRRESTSAEEDIIDGFAMTSFVTFEALEKDVAVKPQERAEKRQTPLTKKKREALTNGLSFHSKKSRLSHSHHYSSDRENDRNLCQHLGKRKKMPKGLRQLKPGQNSCRDSDSESASGESKGFQRSSSRERLSDSSAPSSLGTGYFCDSDSDQEEKASDASSEKLFNTVLVNKDPELGVGALPEHNQDAGPIVPKISGLERSQEKSQDCCKEPVFEPVVLKDPHPQLPQLPSQAQAEPQLQIPSPGPDLVPRTEAPPQFPPPSTQPAQGPPEAQLQPAPLPQVQQRPPRPQSPSHLLQQTLPPVQSHPSSQSLSQPLSAYNSSSLSLNSLSSRSSTPAKTQPAPPHISHHPSASPFPLSLPNHSPLHSFTPTLQPPAHSHHPNMFAPPTALPPPPPLTSGSLQVPGHPAGSTYSEQDILRQELNTRFLASQSADRGASLGPPPYLRTEFHQHQHQHQHTHQHTHQHTFTPFPHAIPPTAIMPTPAPPMFDKYPTKVDPFYRHSLFHSYPPAVSGIPPMIPPTGPFGSLQGAFQPKTSNPIDVAARPGTVPHTLLQKDPRLTDPFRPMLRKPGKWCAMHVHIAWQIYHHQQKVKKQMQSDPHKLDFGLKPEFLSRPPGPSLFGAIHHPHDLARPSTLFSAAGAAHPTGTPFGPPPHHSNFLNPAAHLEPFNRPSTFTGLAAVGGNAFGGLGNPSVTPNSVFGHKDSPSVQNFSNPHEPWNRLHRTPPSFPTPPPWLKPGELERSASAAAHDRDRDVDKRDSSVSKDDKERESVEKRHPSHPSPAPPVPVSALGHNRSSTDPTTRGHLNTEAREKDKPKEKERDHSGSRKDLTTEEHKAKESHLPERDGHSHEGRAAGEEPKQLSRVPSPYVRTPGVDSTRPNSTSSREAEPRKGEPAYENPKKNAEVKVKEERKEDHDLPTEAPQAHRTSEAPPPSSSASASVHPGPLASMPMTVGVTGIHAMNSIGSLDRTRMVTPFMGLSPIPGGERFPYPSFHWDPMRDPLRDPYRDLDMHRRDPLGRDFLLRNDPLHRLSTPRLYEADRSFRDREPHDYSHHHHHHHHPLAVDPRREHERGGHLDERERLHVLREDYEHPRLHPVHPASLDGHLPHPSLLTPGLPSMHYPRISPTAGHQNGLLNKTPPTAALSAPPPLISTLGGRPGSPRRTTPLSAEIRERPPSHTLKDIEAR"


class Cql:
    def __init__(self):
        pass

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
        connection.setup([server], "macpep")
        sync_table(Peptide)
        sync_table(Protein)

    def upsert_peptide(self, server: str, p: Peptide):
        connection.setup([server], "macpep")
        p.validate()
        attrs = p._as_dict()
        # This seems to do it in one command, instead of SELECT + Create/Update
        Peptide.objects(
            partition=attrs["partition"],
            mass=attrs["mass"],
            sequence=attrs["sequence"],
        ).update(
            proteins__add=attrs["proteins"],
            length=attrs["length"],
            number_of_missed_cleavages=attrs["number_of_missed_cleavages"],
            a_count=attrs["a_count"],
            b_count=attrs["b_count"],
            c_count=attrs["c_count"],
            d_count=attrs["d_count"],
            e_count=attrs["e_count"],
            f_count=attrs["f_count"],
            g_count=attrs["g_count"],
            h_count=attrs["h_count"],
            i_count=attrs["i_count"],
            j_count=attrs["j_count"],
            k_count=attrs["k_count"],
            l_count=attrs["l_count"],
            m_count=attrs["m_count"],
            n_count=attrs["n_count"],
            o_count=attrs["o_count"],
            p_count=attrs["p_count"],
            q_count=attrs["q_count"],
            r_count=attrs["r_count"],
            s_count=attrs["s_count"],
            t_count=attrs["t_count"],
            u_count=attrs["u_count"],
            v_count=attrs["v_count"],
            w_count=attrs["w_count"],
            y_count=attrs["y_count"],
            z_count=attrs["z_count"],
            n_terminus=attrs["n_terminus"],
            c_terminus=attrs["c_terminus"],
            is_metadata_up_to_date=attrs["is_metadata_up_to_date"],
        )

    def insert_loop(self, server: str, elements: int):
        connection.setup([server], "macpep")
        for _ in range(elements):
            partition = random.randint(0, 1000)
            mass = random.randint(0, 1000000000)
            sequence = "".join(random.choices(string.ascii_uppercase, k=10))
            Peptide(
                partition=partition, mass=mass, sequence=sequence, proteins={protein}
            ).save()

    def insert_test(self, server: str):
        connection.setup([server], "macpep")
        self.upsert_peptide(
            server,
            Peptide(
                partition=0,
                mass=502286345739,
                sequence="QLSR",
                proteins={protein},
                length=4,
                number_of_missed_cleavages=0,
                n_terminus=0,
                c_terminus=0,
            ),
        )
        # Peptide(
        #     partition=2, mass=945474040024, sequence="SQRDRER", proteins={protein}
        # ).save()
        # Peptide(
        #     partition=8,
        #     mass=3684549317922,
        #     sequence="ERLSDSSAPSSLGTGYFCDSDSDQEEKASDASSEK",
        #     proteins={protein},
        # ).save()
        # Peptide(
        #     partition=5,
        #     mass=2529289540729,
        #     sequence="AGLGTGAAGGIGAGRTRAPSLASSSGSDK",
        #     proteins={protein},
        # ).save()
        # Peptide(
        #     partition=6,
        #     mass=2947478329205,
        #     sequence="ISGLERSQEKSQDCCKEPVFEPVVLK",
        #     proteins={protein},
        # ).save()
        # Peptide(
        #     partition=7,
        #     mass=3018410767455,
        #     sequence="DREPHDYSHHHHHHHHPLAVDPRR",
        #     proteins={protein},
        # ).save()
        # Peptide(
        #     partition=9,
        #     mass=3841096254963,
        #     sequence="ISPTAGHQNGLLNKTPPTAALSAPPPLISTLGGRPGSPR",
        #     proteins={protein},
        # ).save()
        # Peptide(
        #     partition=4,
        #     mass=1614738647319,
        #     sequence="EDHDLPTEAPQAHR",
        #     proteins={protein},
        # ).save()
        # Peptide(
        #     partition=3,
        #     mass=1612755360019,
        #     sequence="SASAAAHDRDRDVDK",
        #     proteins={protein},
        # ).save()
        # Peptide(
        #     partition=1, mass=589307140804, sequence="SSTPAK", proteins={protein}
        # ).save()
