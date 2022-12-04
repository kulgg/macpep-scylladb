from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Peptide(Model):
    __table_name__ = "peptides"

    partition = columns.SmallInt(primary_key=True)
    mass = columns.BigInt(primary_key=True)
    sequence = columns.Text(primary_key=True)
    proteins = columns.Set(columns.Text)
    length = columns.SmallInt()
    number_of_missed_cleavages = columns.SmallInt()
    a_count = columns.SmallInt(default=0)
    b_count = columns.SmallInt(default=0)
    c_count = columns.SmallInt(default=0)
    d_count = columns.SmallInt(default=0)
    e_count = columns.SmallInt(default=0)
    f_count = columns.SmallInt(default=0)
    g_count = columns.SmallInt(default=0)
    h_count = columns.SmallInt(default=0)
    i_count = columns.SmallInt(default=0)
    j_count = columns.SmallInt(default=0)
    k_count = columns.SmallInt(default=0)
    l_count = columns.SmallInt(default=0)
    m_count = columns.SmallInt(default=0)
    n_count = columns.SmallInt(default=0)
    o_count = columns.SmallInt(default=0)
    p_count = columns.SmallInt(default=0)
    q_count = columns.SmallInt(default=0)
    r_count = columns.SmallInt(default=0)
    s_count = columns.SmallInt(default=0)
    t_count = columns.SmallInt(default=0)
    u_count = columns.SmallInt(default=0)
    v_count = columns.SmallInt(default=0)
    w_count = columns.SmallInt(default=0)
    y_count = columns.SmallInt(default=0)
    z_count = columns.SmallInt(default=0)
    n_terminus = columns.SmallInt()
    c_terminus = columns.SmallInt()
    is_metadata_up_to_date = columns.Boolean(default=False)
