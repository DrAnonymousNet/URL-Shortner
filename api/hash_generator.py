import hashlib, random, string
from typing import Union

from django.http import HttpRequest
from django.contrib.auth import get_user_model

User = get_user_model()

def random_md5(url:str, owner:Union[User, None]=None) ->str:
    value = url+str(owner)
    hashes = hashlib.md5(value.encode("utf-8"))
    hash = hashes.hexdigest()[:6]
    return hash

def build_full_url(request:HttpRequest) -> str:
    scheme = request.is_secure() and "https" or "http"
    base_url = f'{scheme}://{request.get_host()}'
    return base_url
