# src/core/cache_decorator.py
import functools
from typing import Any, Callable, Awaitable, Type
from redis.asyncio import Redis
from .base import get_or_set


def cacheable(
    *,
    ttl: int,
    key_builder: Callable[..., str],
    model_cls: Type | None = None,
):
    def decorator(func: Callable[..., Awaitable[Any]]):

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if not args:
                raise RuntimeError("cacheable باید روی متد کلاس (self, ...) استفاده شود.")

            self = args[0]
            redis: Redis | None = getattr(self, "redis", None)
            if redis is None:
                raise RuntimeError("self.redis پیدا نشد.")

            key = key_builder(*args, **kwargs)

            async def loader():
                result = await func(*args, **kwargs)
                if model_cls is not None and hasattr(result, "model_dump"):
                    return result.model_dump()
                return result

            data = await get_or_set(redis=redis, key=key, ttl=ttl, loader=loader)

            if model_cls is not None and isinstance(data, dict):
                return model_cls(**data)

            return data

        return wrapper

    return decorator
