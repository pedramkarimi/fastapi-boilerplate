from redis.asyncio import Redis
from src.core.config import settings

_redis: Redis | None = None

async def init_redis():
    global _redis
    _redis = Redis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
    )

async def close_redis():
    global _redis
    if _redis:
        await _redis.close()
        _redis = None

async def get_redis() -> Redis:
    assert _redis is not None, "Redis is not initialized"
    return _redis
