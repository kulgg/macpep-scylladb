from io import TextIOWrapper


class UniprotDigest:
    def __init__(self):
        pass

    def digest(self, path: str):
        f = open(path, "r")
        a = self.get_next_protein(f)
        print(a)
        f.close()

    def get_next_protein(self, f: TextIOWrapper) -> str:
        protein = ""
        line = f.readline()

        while line != "//\n":
            protein += line
            line = f.readline()

        return protein


"""
Get all // separated proteins
Get all protein info fields
Digest Sequence
"""
