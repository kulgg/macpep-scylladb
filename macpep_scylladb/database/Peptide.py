from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Peptide(Model):
    __table_name__ = "peptides"

    partition = columns.SmallInt(primary_key=True, required=True)
    mass = columns.BigInt(primary_key=True, required=True)
    c_count = columns.SmallInt(primary_key=True, default=0, required=True)
    m_count = columns.SmallInt(primary_key=True, default=0, required=True)
    s_count = columns.SmallInt(primary_key=True, default=0, required=True)
    t_count = columns.SmallInt(primary_key=True, default=0, required=True)
    y_count = columns.SmallInt(primary_key=True, default=0, required=True)
    n_terminus = columns.SmallInt(primary_key=True, required=True)
    c_terminus = columns.SmallInt(primary_key=True, required=True)
    r_count = columns.SmallInt(primary_key=True, default=0, required=True)
    k_count = columns.SmallInt(primary_key=True, default=0, required=True)
    a_count = columns.SmallInt(primary_key=True, default=0, required=True)
    b_count = columns.SmallInt(primary_key=True, default=0, required=True)
    d_count = columns.SmallInt(primary_key=True, default=0, required=True)
    e_count = columns.SmallInt(primary_key=True, default=0, required=True)
    f_count = columns.SmallInt(primary_key=True, default=0, required=True)
    g_count = columns.SmallInt(primary_key=True, default=0, required=True)
    h_count = columns.SmallInt(primary_key=True, default=0, required=True)
    i_count = columns.SmallInt(primary_key=True, default=0, required=True)
    j_count = columns.SmallInt(primary_key=True, default=0, required=True)
    l_count = columns.SmallInt(primary_key=True, default=0, required=True)
    n_count = columns.SmallInt(primary_key=True, default=0, required=True)
    o_count = columns.SmallInt(primary_key=True, default=0, required=True)
    p_count = columns.SmallInt(primary_key=True, default=0, required=True)
    q_count = columns.SmallInt(primary_key=True, default=0, required=True)
    u_count = columns.SmallInt(primary_key=True, default=0, required=True)
    v_count = columns.SmallInt(primary_key=True, default=0, required=True)
    w_count = columns.SmallInt(primary_key=True, default=0, required=True)
    z_count = columns.SmallInt(primary_key=True, default=0, required=True)
    sequence = columns.Text(required=True)
    proteins = columns.Set(columns.Text, required=True)
    length = columns.SmallInt(required=True)
    number_of_missed_cleavages = columns.SmallInt(required=True)
    is_metadata_up_to_date = columns.Boolean(default=False, required=True)
    is_swiss_prot = columns.Boolean(default=False, required=True)
    is_trembl = columns.Boolean(default=False, required=True)
    taxonomy_ids = columns.Set(columns.Integer, required=True, default=[])
    unique_taxonomy_ids = columns.Set(columns.Integer, required=True, default=[])
    proteome_ids = columns.Set(columns.Text, required=True, default=[])
