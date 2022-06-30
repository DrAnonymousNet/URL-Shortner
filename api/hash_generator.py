import hashlib, random, string


def random_md5(url, owner=None):
    hash_list = []
    value = url+str(owner)
    hashes = hashlib.md5(value.encode("utf-8"))
    hash_list.append(hashes.hexdigest()[:6])
    return hash_list