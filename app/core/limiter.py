import os
from slowapi import Limiter
from slowapi.util import get_remote_address

if os.getenv("TESTING"):
    limiter = Limiter(key_func=get_remote_address, default_limits=[])
else:
    limiter = Limiter(key_func=get_remote_address)