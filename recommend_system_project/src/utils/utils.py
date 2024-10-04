import hashlib

HASH_LIB = hashlib.sha256()


def hash_string(input_string: str):
    HASH_LIB = hashlib.sha256()
    HASH_LIB.update(input_string.encode("utf-8"))
    return HASH_LIB.hexdigest()


if __name__ == "__main__":
    print(hash_string("hello"))
