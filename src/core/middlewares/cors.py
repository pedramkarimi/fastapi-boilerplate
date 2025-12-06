from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings


def setup_cors(app: FastAPI) -> None:
    if not settings.BACKEND_CORS_ORIGINS:
        return

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],   # ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        allow_headers=["*"],   # ["Authorization", "Content-Type", "Accept"]
        # expose_headers=["Content-Disposition"],   # send file to front
    )
