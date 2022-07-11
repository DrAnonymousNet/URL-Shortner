import hashlib, random, string


def random_md5(url, owner=None):
    value = url+str(owner)
    hashes = hashlib.md5(value.encode("utf-8"))
    hash = hashes.hexdigest()[:6]
    return hash