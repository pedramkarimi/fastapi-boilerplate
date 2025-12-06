from fastapi import FastAPI
from .logging import logging_middleware
from .cors import setup_cors

def setup_middlewares(app: FastAPI):
    setup_cors(app)
    app.middleware("http")(logging_middleware)