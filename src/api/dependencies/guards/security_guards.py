from fastapi import Depends, Request
from redis.asyncio import Redis
from src.core.redis import get_redis
from src.core.exceptions import TooManyRequestsException
from src.api.v1.auth.schemas import LoginRequest
from src.api.v1.auth.login_attempt_service import LoginAttemptService
from src.api.dependencies.utils import get_client_ip
from src.core.errors import ErrorMessages


def get_login_attempt_service(redis: Redis = Depends(get_redis)) -> LoginAttemptService:
    return LoginAttemptService(redis=redis)


async def login_bruteforce_guard(
    credentials: LoginRequest,
    request: Request,
    attempts: LoginAttemptService = Depends(get_login_attempt_service),
) -> None:
    ip = get_client_ip(request)
    email = credentials.email.lower()

    if await attempts.is_locked(email=email, ip=ip):
        raise TooManyRequestsException(ErrorMessages.TOO_MANY_FAILED_LOGIN)