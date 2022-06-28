from decouple import config
from .base import *

if config('ENVIRONMENT') == "PRODUCTION":
    from .production import *

else:
    from .development import *