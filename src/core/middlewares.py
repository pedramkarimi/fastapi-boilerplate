# app/core/middlewares.py

import time
import logging
from typing import Callable

from fastapi import Request, Response
from fastapi import HTTPException

from .exceptions import AppException
from .handlers import (
    app_exception_handler,
    http_exception_handler,
    generic_exception_handler,
)
from .log_models import RequestLog
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger("app.request")


def get_client_ip(request: Request) -> str | None:
    return request.client.host if request.client else None

async def logging_middleware(request: Request, call_next: Callable) -> Response:
    start_time = time.perf_counter()

    # اگر بعداً auth داشتی، می‌تونی تو dependency user رو تو request.state.user بذاری
    user_id: str | None = getattr(request.state, "user_id", None)

    try:
        # سعی می‌کنیم درخواست عادی را پردازش کنیم
        response = await call_next(request)
        status_code = response.status_code
        error_code = None
        error_message = None

    except AppException as exc:
        # خطاهای دامینی خودمون
        status_code = exc.status_code
        error_code = exc.code
        error_message = exc.message
        # response رو هم با همون handler استاندارد بسازیم:
        response = await app_exception_handler(request, exc)

    except HTTPException as exc:
        status_code = exc.status_code
        error_code = None
        error_message = str(exc.detail)
        response = await http_exception_handler(request, exc)

    except Exception as exc:
        status_code = 500
        if isinstance(exc, SQLAlchemyError):
            error_code = "DB_ERROR"
        else:
            error_code = None

        error_message = f"{exc.__class__.__name__}: {exc}"
        error_code = None
        response = await generic_exception_handler(request, exc)

    duration_ms = (time.perf_counter() - start_time) * 1000

    log_entry = RequestLog(
        method=request.method,
        path=request.url.path,
        status_code=status_code,
        duration_ms=duration_ms,
        client_ip=get_client_ip(request),
        user_id=user_id,
        error_code=error_code,
        error_message=error_message,
        extra={},  # اگر چیزی خواستی اضافه کنی
    )

    # فقط خطاها رو به صورت ERROR لاگ کنیم، موفق‌ها را یا نادیده بگیر یا در سطح دیگری
    if status_code >= 500:
        logger.error(log_entry.model_dump())
    elif status_code >= 400:
        logger.warning(log_entry.model_dump())
    # اگر خواستی، اینجا می‌تونی برای 2xx هم بر اساس sampling لاگ بگیری

    return response
