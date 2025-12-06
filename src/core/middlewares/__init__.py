from fastapi import FastAPI
from .logging import logging_middleware
from .cors import setup_cors
from .rate_limit import rate_limit_middleware

def setup_middlewares(app: FastAPI):
    setup_cors(app)
    app.middleware("http")(rate_limit_middleware)
    app.middleware("http")(logging_middleware)