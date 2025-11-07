from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import FastAPI
from .config import settings

limiter = Limiter(key_func=get_remote_address)

def init_middlewares(app: FastAPI):
    app.state.limiter = limiter
    app.add_exception_handler(429, _rate_limit_exceeded_handler)
