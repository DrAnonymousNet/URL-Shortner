import hashlib, random, string


def random_md5(url, owner=None):
    value = url+str(owner)
    hashes = hashlib.md5(value.encode("utf-8"))
    hash = hashes.hexdigest()[:6]
    return hash

def build_full_url(request):
    scheme = request.is_secure() and "https" or "http"
    base_url = f'{scheme}://{request.get_host()}'
    return base_url
