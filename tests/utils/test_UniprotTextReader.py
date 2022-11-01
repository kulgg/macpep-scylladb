from macpep_scylladb.models.Protein import Protein
from macpep_scylladb.utils.UniprotTextReader import UniprotTextReader
from testfixtures import compare


def test_next_should_return_test_protein():
    # Arrange
    expected = Protein(
        accession="A0A088MLT8",
        secondary_accessions=[
            "A8IJC6",
            "A8IJD0",
            "A8IJD3",
            "F6YL02",
            "F8WI70",
            "Q3TI53",
            "Q52KH1",
            "Q6P9Y8",
            "Q9CX07",
            "Q9JLR0",
        ],
        entry_name="IQIP1_MOUSE",
        name="IQCJ-SCHIP1 readthrough transcript protein",
        sequence=(
            "MRLEELKRLQNPLEQVDDGKYLLENHQLAMDVENNIENYPLSLQPLESKVKIIQRAWREYLQRQDPLEKRSPS"
            "PPSVSSDKLSSSVSMNTFSDSSTPDYREDGMDLGSDAGSSSSSRASSQSNSTKVTPCSECKSSSSPGGSLDLV"
            "SALEDYEEPFPVYQKKVIDEWAPEEDGEEEEEEDDRGYRDDGCPAREPGDVSARIGSSGSGSRSAATTMPSPM"
            "PNGNLHPHDPQDLRHNGNVVVAGRPNASRVPRRPIQKTQPPGSRRGGRNRASGGLCLQPPDGGTRVPEEPPAP"
            "PMDWEALEKHLAGLQFREQEVRNQGQARTNSTSAQKNERESIRQKLALGSFFDDGPGIYTSCSKSGKPSLSAR"
            "LQSGMNLQICFVNDSGSDKDSDADDSKTETSLDTPLSPMSKQSSSYSDRDTTEEESESLDDMDFLTRQKKLQA"
            "EAKMALAMAKPMAKMQVEVEKQNRKKSPVADLLPHMPHISECLMKRSLKPTDLRDMTIGQLQVIVNDLHSQIE"
            "SLNEELVQLLLIRDELHTEQDAMLVDIEDLTRHAESQQKHMAEKMPAK"
        ),
        taxonomy_id=10090,
        proteome_id="UP000000589",
        is_reviewed=True,
        updated_at=1659484800.0,
    )

    # Act / Assert
    with open("tests/utils/protein.txt", "r") as protein_file:
        reader = UniprotTextReader(protein_file)
        proteins = []

        for protein in reader:
            proteins.append(protein)

        assert len(proteins) == 1
        compare(proteins[0], expected)
