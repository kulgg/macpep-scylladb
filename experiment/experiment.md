# Experiments

## First Experiment - MusMucus

### Config

Using Docker in both instances.
Single node for scylla.

### Results

Scylla
17,568 proteins
2,532,960 Peptides
20 Mins
14.86P/sec
329.59 MB Size

Postgres
17,568 proteins
2,392,230 peptides
19 mins
-> 15.41 P/s
Update 11 mins
12 MB Size

No idea what is going on

## Experiment - Greate Apes

### Config

Nodes

```
macpepdb-01 192.168.0.242
macpepdb-02 192.168.0.158
macpepdb-03 192.168.0.102
macpepdb-04 192.168.0.132
macpepdb-05 192.168.0.65
```

Scylla Config

- 5 Nodes
- GossipingPropertyFileSnitch
- One datacenter
- No Docker
- RAID / XFS partition?
- did not choose some of the optimization options. Might be even better

Cluster

- Deployed Scylla cluster with
  - https://www.scylladb.com/download/?platform=ubuntu-22.04&version=scylla-5.1#open-source
  - https://docs.scylladb.com/stable/operating-scylla/procedures/cluster-management/create-cluster.html

### Results

## Scylla

- Partition generation 6 hours 8 mins -> 711 Partitions
- Experiment command `poetry run x inserter run_multi 192.168.0.242 data/great-ape-1000.txt data/uniprot-great-apes.txt --num_threads 14`
- Start date: 2023-01-20 09:21:41,286 [INFO] Inserter.run_multi(): Total proteins: 529820
- Processing |############################### | 529817/529820 Proteins 18.44P/sec 54111831 Peptides2023-01-20 17:20:37,146 [INFO] Inserter.run_multi(): Number of proteins: 529820
  2023-01-20 17:20:37,146 [INFO] Inserter.run_multi(): Number of peptides: 54112252
