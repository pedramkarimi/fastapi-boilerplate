import json
from typing import Any, Callable, Awaitable
from redis.asyncio import Redis

async def get_or_set(
    redis: Redis,
    key: str,
    ttl: int,
    loader: Callable[[], Awaitable[Any]],
):
    cached_value = await redis.get(key)

    if cached_value is not None:
        return json.loads(cached_value)

    data = await loader()
    await redis.set(key, json.dumps(data), ex=ttl)
    return data
