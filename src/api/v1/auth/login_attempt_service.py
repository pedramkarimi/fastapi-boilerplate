from redis.asyncio import Redis
from src.core.config import settings
from src.core.redis_keys import RedisKeys

class LoginAttemptService:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def is_locked(self, email: str, ip: str) -> bool:
        email = email.lower()
        email_lock_key = RedisKeys.brute_force_email_lock(email)
        ip_lock_key = RedisKeys.brute_force_ip_lock(ip)

        exists_count = await self.redis.exists(email_lock_key, ip_lock_key)
        return exists_count > 0


    async def register_failed_attempt(self, email: str, ip: str) -> None:
        email = email.lower()
        
        email_attempts_key = RedisKeys.brute_force_email_attempts(email)
        ip_attempts_key = RedisKeys.brute_force_ip_attempts(ip)

        email_attempts = await self.redis.incr(email_attempts_key)
        if email_attempts == 1:
            await self.redis.expire(email_attempts_key, settings.LOGIN_ATTEMPT_WINDOW_SECONDS)

        ip_attempts = await self.redis.incr(ip_attempts_key)
        if ip_attempts == 1:
            await self.redis.expire(ip_attempts_key, settings.LOGIN_ATTEMPT_WINDOW_SECONDS)

        if email_attempts >= settings.LOGIN_MAX_ATTEMPTS_PER_EMAIL:
            await self.redis.set(RedisKeys.brute_force_email_lock(email), "1", ex=settings.LOGIN_LOCK_TTL_SECONDS)

        if ip_attempts >= settings.LOGIN_MAX_ATTEMPTS_PER_IP:
            await self.redis.set(RedisKeys.brute_force_ip_lock(ip), "1", ex=settings.LOGIN_LOCK_TTL_SECONDS)
        

    async def reset_attempts(self, email: str, ip: str) -> None:
        email = email.lower()
        keys = [
            RedisKeys.brute_force_email_attempts(email),
            RedisKeys.brute_force_ip_attempts(ip),
            RedisKeys.brute_force_email_lock(email),
            RedisKeys.brute_force_ip_lock(ip)
        ]
        await self.redis.delete(*keys)
