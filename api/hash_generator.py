import hashlib, random, string


def random_md5(url):
    hash_list = []
    hashes = hashlib.md5(url.encode("utf-8"))
    hash_list.append(hashes.hexdigest()[:6])
    return hash_list