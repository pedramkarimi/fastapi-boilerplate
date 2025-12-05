from fastapi import FastAPI, HTTPException, Depends
from .api.v1.router import router as api_v1_router
from fastapi.exceptions import RequestValidationError
from .core.exceptions import AppException
from .core.handlers import (
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from src.core.middlewares import logging_middleware
from src.core.redis import init_redis, close_redis
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis()   
    print("Redis initialized.")

    yield  

    await close_redis()
    print("Redis closed.")

app = FastAPI(debug=True, lifespan=lifespan)
app.include_router(api_v1_router, prefix="/api/v1")

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(AppException, app_exception_handler)

app.middleware("http")(logging_middleware)


