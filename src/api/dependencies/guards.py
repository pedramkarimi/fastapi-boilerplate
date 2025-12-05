from fastapi import Depends, Request
from .deps import get_current_user_data
from .models import AuthenticatedUser
from redis.asyncio import Redis
from src.core.redis import get_redis
from src.core.exceptions import TooManyRequestsException
from src.api.v1.auth.schemas import LoginRequest
from src.api.v1.auth.login_attempt_service import LoginAttemptService

def AuthGuard() -> AuthenticatedUser:
    def wrapper(current_user = Depends(get_current_user_data)) -> AuthenticatedUser:
        return AuthenticatedUser(
            id=current_user.id,
            email=current_user.email
        )
    return Depends(wrapper)

def get_login_attempt_service(redis: Redis = Depends(get_redis)) -> LoginAttemptService:
    return LoginAttemptService(redis=redis)


async def login_bruteforce_guard(
    credentials: LoginRequest,
    request: Request,
    attempts: LoginAttemptService = Depends(get_login_attempt_service),
) -> None:
    ip = request.client.host if request.client else "unknown"
    email = credentials.email.lower()

    if await attempts.is_locked(email=email, ip=ip):
        raise TooManyRequestsException(
            "Too many failed login attempts. Please try again later."
        )