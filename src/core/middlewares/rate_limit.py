# src/core/middleware/rate_limit.py
from __future__ import annotations
import time
from typing import Callable, Awaitable
from fastapi import Request, Response, HTTPException
from redis.exceptions import RedisError
from src.core.redis import get_redis
from src.api.dependencies.utils import get_client_ip  
from src.core.config import settings
from src.core.redis_keys import RedisKeys
from src.core.errors import ErrorMessages
from src.core.exceptions import TooManyRequestsException


def _get_rate_limit_for_path(path: str) -> tuple[int | None, int]:
    # مثال: روی docs و openapi محدودیت نذار
    if path.startswith("/docs") or path.startswith("/redoc") or path.startswith("/openapi.json"):
        return None, settings.RATELIMIT_DEFAULT_WINDOW_SECONDS

    return settings.RATELIMIT_DEFAULT_MAX_REQUESTS, settings.RATELIMIT_DEFAULT_WINDOW_SECONDS


async def rate_limit_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    path = request.url.path
    ip = get_client_ip(request)

    max_requests, window_seconds = _get_rate_limit_for_path(path)
    if max_requests is None:
        return await call_next(request)

    redis_key = RedisKeys.rate_limit_ip(ip=ip, path=path)

    try:
        redis = await get_redis()

        current_count = await redis.incr(redis_key)
        if current_count == 1:
            await redis.expire(redis_key, window_seconds)

        if current_count > max_requests:
            raise TooManyRequestsException(ErrorMessages.TOO_MANY_REQUESTS)

    except RedisError:
        pass

    response = await call_next(request)
    return response
