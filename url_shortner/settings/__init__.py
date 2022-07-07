from decouple import config
from .base import *

if config('ENVIRONMENT') == "PRODUCTION":
    from .production import *
elif  config('ENVIRONMENT') == "PRODUCTIONH":
    from .productionheroku import *

else:
    from .development import *