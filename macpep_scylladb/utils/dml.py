from typing import List
from cassandra.cqlengine.query import BatchStatement
from cassandra.query import BatchType
from cassandra.concurrent import execute_concurrent
from macpep_scylladb.database.Peptide import Peptide
from macpep_scylladb.database.Protein import Protein
from cassandra.cluster import Session
from cassandra import ConsistencyLevel
from cassandra.policies import ConstantReconnectionPolicy


def insert_proteins(session, proteins: List[Protein]):
    insert_statement_str = """INSERT INTO macpep.proteins ("accession", "secondary_accessions", "entry_name", "name", "sequence", "taxonomy_id", "proteome_id", "is_reviewed", "updated_at") VALUES (?,?,?,?,?,?,?,?,?)"""
    insert_statement = session.prepare(insert_statement_str)

    statements_and_params = []
    for p in proteins:
        params = (
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


def batch_upsert_peptides(session: Session, peptides: List[Peptide]):
    update_statement_str = """UPDATE macpep.peptides SET "proteins" = "proteins" + ?, "length" = ?, "number_of_missed_cleavages" = ?, "a_count" = ?, "b_count" = ?, "c_count" = ?, "d_count" = ?, "e_count" = ?, "f_count" = ?, "g_count" = ?, "h_count" = ?, "i_count" = ?, "j_count" = ?, "k_count" = ?, "l_count" = ?, "m_count" = ?, "n_count" = ?, "o_count" = ?, "p_count" = ?, "q_count" = ?, "r_count" = ?, "s_count" = ?, "t_count" = ?, "u_count" = ?, "v_count" = ?, "w_count" = ?, "y_count" = ?, "z_count" = ?, "n_terminus" = ?, "c_terminus" = ?  WHERE "partition" = ? AND "mass" = ? AND "sequence" = ?"""
    update_statement = session.prepare(update_statement_str)
    batch = BatchStatement(
        BatchType.UNLOGGED,
        retry_policy=ConstantReconnectionPolicy(0.1),
        consistency_level=ConsistencyLevel.ONE,
    )

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
            # p.is_metadata_up_to_date,
            # p.taxonomy_ids,
            # p.unique_taxonomy_ids,
            # p.proteome_ids,
            # ', "is_swiss_prot" = True ' if p.is_swiss_prot else "",
            p.partition,
            p.mass,
            p.sequence,
        )
        batch.add(update_statement, params)

    session.execute(batch)


def upsert_peptides(session, peptides: List[Peptide]):
    # Using execute_concurrent with the same UPDATE statement that upsert_peptides uses under the hood is significantly faster
    update_statement_str = """UPDATE macpep.peptides SET "proteins" = "proteins" + ?, "length" = ?, "number_of_missed_cleavages" = ?, "a_count" = ?, "b_count" = ?, "c_count" = ?, "d_count" = ?, "e_count" = ?, "f_count" = ?, "g_count" = ?, "h_count" = ?, "i_count" = ?, "j_count" = ?, "k_count" = ?, "l_count" = ?, "m_count" = ?, "n_count" = ?, "o_count" = ?, "p_count" = ?, "q_count" = ?, "r_count" = ?, "s_count" = ?, "t_count" = ?, "u_count" = ?, "v_count" = ?, "w_count" = ?, "y_count" = ?, "z_count" = ?, "n_terminus" = ?, "c_terminus" = ?  WHERE "partition" = ? AND "mass" = ? AND "sequence" = ?"""
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
            # p.is_metadata_up_to_date,
            # p.taxonomy_ids,
            # p.unique_taxonomy_ids,
            # p.proteome_ids,
            # ', "is_swiss_prot" = True ' if p.is_swiss_prot else "",
            p.partition,
            p.mass,
            p.sequence,
        )
        statements_and_params.append((update_statement, params))

    execute_concurrent(session, statements_and_params, raise_on_first_error=True)


def upsert_peptide(session: Session, p: Peptide):
    # Using execute_concurrent with the same UPDATE statement that upsert_peptides uses under the hood is significantly faster
    update_statement_str = """UPDATE macpep.peptides SET "proteins" = "proteins" + ?, "length" = ?, "number_of_missed_cleavages" = ?, "a_count" = ?, "b_count" = ?, "c_count" = ?, "d_count" = ?, "e_count" = ?, "f_count" = ?, "g_count" = ?, "h_count" = ?, "i_count" = ?, "j_count" = ?, "k_count" = ?, "l_count" = ?, "m_count" = ?, "n_count" = ?, "o_count" = ?, "p_count" = ?, "q_count" = ?, "r_count" = ?, "s_count" = ?, "t_count" = ?, "u_count" = ?, "v_count" = ?, "w_count" = ?, "y_count" = ?, "z_count" = ?, "n_terminus" = ?, "c_terminus" = ?  WHERE "partition" = ? AND "mass" = ? AND "sequence" = ?"""
    update_statement = session.prepare(update_statement_str)

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
        # p.is_metadata_up_to_date,
        # p.taxonomy_ids,
        # p.unique_taxonomy_ids,
        # p.proteome_ids,
        # ', "is_swiss_prot" = True ' if p.is_swiss_prot else "",
        p.partition,
        p.mass,
        p.sequence,
    )
    session.execute_async(update_statement, params)
