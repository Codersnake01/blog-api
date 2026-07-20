import os
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# Desactivar completamente el rate limiting durante los tests
if os.getenv("PYTEST_CURRENT_TEST"):
    limiter.enabled = False