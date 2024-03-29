from __future__ import annotations

from macpep_scylladb.proteomics.mass import to_int as mass_to_int

AMINO_ACIDS_FOR_COUNTING = [
    "A",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "Y",
]


class AminoAcid:
    """
    Defines an amino acid.

    Parameters
    ----------
    name : str
        Full name
    one_letter_code : str
        One letter code
    three_letter_code : str
        Three letter code
    chemical_formula : str
        Chemical formular
    mono_mass : float
        Mono mass in human readable float (Dalton)
    average_mass : float
        Average mass in human readable float (Dalton)
    """

    def __init__(
        self,
        name: str,
        one_letter_code: str,
        three_letter_code: str,
        chemical_formula: str,
        mono_mass: float,
        average_mass: float,
    ):
        self.name = name
        self.one_letter_code = one_letter_code
        self.three_letter_code = three_letter_code
        self.chemical_formula = chemical_formula
        self.mono_mass = mass_to_int(mono_mass)
        self.average_mass = mass_to_int(average_mass)

    def __hash__(self) -> int:
        return hash(self.one_letter_code)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AminoAcid):
            return NotImplemented

        return self.one_letter_code == other.one_letter_code

    def get_one_letter_code_ascii_dec(self) -> int:
        """
        Returns
        -------
        Decimal ASCII represenation of the amino acids one letter code
        """
        return ord(self.one_letter_code)

    @classmethod
    def get_by_one_letter_code(cls, one_letter_code: str):
        """
        Returns an amino acid by one letter code.

        Parameters
        ----------
        one_letter_code : str
            One letter code of an amino acid.

        Returns
        -------
        Amino acid

        Raises
        ------
        NameError
            If the given one letter code is unknown.
        """
        olc = one_letter_code.upper()
        if olc == "A":
            return A
        elif olc == "C":
            return C
        elif olc == "D":
            return D
        elif olc == "E":
            return E
        elif olc == "F":
            return F
        elif olc == "G":
            return G
        elif olc == "H":
            return H
        elif olc == "I":
            return I
        elif olc == "K":
            return K
        elif olc == "L":
            return L
        elif olc == "M":
            return M
        elif olc == "N":
            return N
        elif olc == "O":
            return O
        elif olc == "P":
            return P
        elif olc == "Q":
            return Q
        elif olc == "R":
            return R
        elif olc == "S":
            return S
        elif olc == "T":
            return T
        elif olc == "U":
            return U
        elif olc == "V":
            return V
        elif olc == "W":
            return W
        elif olc == "Y":
            return Y
        elif olc == "B":
            return B
        elif olc == "J":
            return J
        elif olc == "Z":
            return Z
        elif olc == "X":
            return X
        else:
            raise NameError(f"No amino acid with one letter code '{olc}' found.")

    @classmethod
    def get_haviest(cls):
        """
        Returns
        -------
        Heaviest amino acis (Tryptophan)
        """
        return W

    @classmethod
    def get_lightest(cls):
        """
        Returns
        -------
        Lightest amino acis (Glycine)
        """
        return G

    @staticmethod
    def get_unknown():
        """
        Returns
        -------
        Unknwon
        """
        return X

    @staticmethod
    def all() -> tuple:
        """
        Returns
        -------
        Tuple with all known amino acids
        """
        return KNOWN_AMINO_ACIDS


# Standard amino acids
# https://proteomicsresource.washington.edu/protocols06/masses.php
A = AminoAcid("Alanine", "A", "Ala", "C3H5ON", 71.037113805, 71.0788)
C = AminoAcid("Cysteine", "C", "Cys", "C3H5ONS", 103.009184505, 103.1388)
D = AminoAcid("Aspartic acid", "D", "Asp", "C4H5O3N", 115.026943065, 115.0886)
E = AminoAcid("Glutamic acid", "E", "Glu", "C5H7O3N", 129.042593135, 129.1155)
F = AminoAcid("Phenylalanine", "F", "Phe", "C9H9ON", 147.068413945, 147.1766)
G = AminoAcid("Glycine", "G", "Gly", "C2H3ON", 57.021463735, 57.0519)
H = AminoAcid("Histidine", "H", "His", "C6H7ON3", 137.058911875, 137.1411)
I = AminoAcid("Isoleucine", "I", "Ile", "C6H11ON", 113.084064015, 113.1594)
K = AminoAcid("Lysine", "K", "Lys", "C6H12ON2", 128.094963050, 128.1741)
L = AminoAcid("Leucine", "L", "Leu", "C6H11ON", 113.084064015, 113.1594)
M = AminoAcid("Methionine", "M", "Met", "C5H9ONS", 131.040484645, 131.1926)
N = AminoAcid("Asparagine", "N", "Asn", "C4H6O2N2", 114.042927470, 114.1038)
O = AminoAcid("Pyrrolysine", "O", "Pyl", "C12H19N3O2", 237.147726925, 237.29816)
P = AminoAcid("Proline", "P", "Pro", "C5H7ON", 97.052763875, 97.1167)
Q = AminoAcid("Glutamine", "Q", "Gln", "C5H8O2N2", 128.05857754, 128.1307)
R = AminoAcid("Arginine", "R", "Arg", "C6H12ON4", 156.101111050, 156.1875)
S = AminoAcid("Serine", "S", "Ser", "C3H5O2N", 87.032028435, 87.0782)
T = AminoAcid("Threonine", "T", "Thr", "C4H7O2N", 101.047678505, 101.1051)
U = AminoAcid("Selenocysteine", "U", "SeC", "C3H5NOSe", 150.953633405, 150.0379)
V = AminoAcid("Valine", "V", "Val", "C5H9ON", 99.068413945, 99.1326)
W = AminoAcid("Tryptophan", "W", "Trp", "C11H10ON2", 186.079312980, 186.2132)
Y = AminoAcid("Tyrosine", "Y", "Tyr", "C9H9O2N", 163.063328575, 163.1760)
# Ambigous amino acids
B = AminoAcid(
    "Asparagine or aspartic acid",
    "B",
    "Asx",
    "C4H6O2N2/C4H5O3N",
    114.5349352675,
    114.59502,
)
J = AminoAcid("Isoleucine or Leucine", "J", "Xle", "C6H11ON", 113.084064015, 113.1594)
Z = AminoAcid(
    "Glutamine or glutamic acid",
    "Z",
    "Glx",
    "C5H8O2N2/C5H7O3N",
    128.5505853375,
    128.6216,
)
# Special amino acids
# Some Search Engines and Databases used the X Amino Acid for unknown amino acids
X = AminoAcid("Unknown Amino Acid", "X", "Xaa", "Unknown", 0.0, 0.0)

# Tuple with containing all standard amino acids and X (unknown)
KNOWN_AMINO_ACIDS = (
    A,
    C,
    D,
    E,
    F,
    G,
    H,
    I,
    K,
    L,
    M,
    N,
    O,
    P,
    Q,
    R,
    S,
    T,
    U,
    V,
    W,
    Y,
    B,
    J,
    Z,
    X,
)

# Lookup for ambigous amino acids where the differentiated amino acids actually have
# varying masses.
# This is true for B and Z.
REPLACEABLE_AMBIGIOUS_AMINO_ACID_LOOKUP = {"B": [D, N], "Z": [E, Q]}
