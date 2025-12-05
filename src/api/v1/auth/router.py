from fastapi import APIRouter, Depends, Request
from .paths import AuthPaths
from .service import AuthService
from .schemas import LoginRequest, TokenResponse
from src.core.response import BaseResponse
from src.api.dependencies.guards.auth_guards import AuthGuard
from src.api.dependencies.guards.security_guards import get_login_attempt_service, login_bruteforce_guard
from src.api.dependencies.models import AuthenticatedUser
from redis.asyncio import Redis
from src.core.redis import get_redis
from .login_attempt_service import LoginAttemptService
from sqlalchemy.orm import Session
from src.db.session import get_db

router = APIRouter()

def get_auth_service(
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    attempts: LoginAttemptService = Depends(get_login_attempt_service),
) -> AuthService:
    return AuthService(db=db, redis=redis, attempts=attempts)


@router.get(AuthPaths.ME, response_model=BaseResponse[AuthenticatedUser])
def read_me(user : AuthenticatedUser = AuthGuard()):
    return BaseResponse[AuthenticatedUser](data=user)


@router.post(AuthPaths.LOGIN, response_model=BaseResponse[TokenResponse])
async def login(request: Request, credentials: LoginRequest, _guard: None = Depends(login_bruteforce_guard), service: AuthService = Depends(get_auth_service)):
    return await service.login(request=request, credentials=credentials)