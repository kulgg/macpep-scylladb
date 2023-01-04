import xxhash


def hash_string(s: str, n: int) -> int:
    h = xxhash.xxh64(s.encode()).intdigest()
    return h * (n - 1) // (2**64 - 1)
