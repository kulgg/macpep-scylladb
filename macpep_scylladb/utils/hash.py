import sys

import xxhash


def hash_string(s: str, n: int) -> int:
    h = xxhash.xxh64(s.encode()).intdigest()
    return h * (n - 1) // (2**64 - 1)


if __name__ == "__main__":
    print(globals()[sys.argv[1]](sys.argv[2], int(sys.argv[3])))
