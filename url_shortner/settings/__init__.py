from decouple import config
from .base import *

if config('ENVIRONMENT') == "PRODUCTION":
    from .production import *
elif  config('ENVIRONMENTH') == "PRODUCTION":
    from .productionheroku import *

else:
    from .development import *