from macpep_scylladb.modules.Partitioner import Partitioner
from macpep_scylladb.modules.Proteomics import Proteomics


def test_get_partition():
    proteomics = Proteomics()
    partitioner = Partitioner(proteomics)

    partitions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]

    mass_to_partition_index = {
        1: 0,
        2: 1,
        3: 2,
        4: 3,
        5: 4,
        6: 5,
        7: 6,
        8: 7,
        9: 8,
        10: 9,
        11: 9,
        12: 9,
        13: 9,
        14: 9,
        15: 10,
        16: 10,
        17: 10,
        18: 10,
        19: 10,
        20: 11,
    }

    for mass, partition_index in mass_to_partition_index.items():
        actual = partitioner.get_partition_index(partitions, mass)
        assert actual == partition_index
