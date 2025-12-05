from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from src.api.v1.user.repository import UserRepository
from .schemas import LoginRequest, TokenResponse
from src.core.response import BaseResponse
from src.core.errors import ErrorMessages
from src.core.security import Security
from src.core.exceptions import InvalidCredentialsException, PermissionDeniedException
from redis.asyncio import Redis
from .login_attempt_service import LoginAttemptService

class AuthService:
    def __init__(self, db: Session, redis: Redis, attempts: LoginAttemptService):
        self.db = db
        self.redis = redis
        self.attempts = attempts
        self.user_repo = UserRepository(db)

    async def login(self, request: Request, credentials: LoginRequest) -> BaseResponse[TokenResponse]:
        ip = request.client.host if request.client else "unknown"
        email = credentials.email.lower()

        user = self.user_repo.get_user_by_email(credentials.email)
        if user is None:
            await self.attempts.register_failed_attempt(email=email, ip=ip)
            raise InvalidCredentialsException(ErrorMessages.INVALID_CREDENTIALS)
        
        password_is_verified = Security.verify_password(credentials.password, user.password)
        if not password_is_verified:
            await self.attempts.register_failed_attempt(email=email, ip=ip)
            raise InvalidCredentialsException(ErrorMessages.INVALID_CREDENTIALS)
        
        if not user.is_active:
            raise PermissionDeniedException(ErrorMessages.USER_IS_INACTIVE)
        
        await self.attempts.reset_attempts(email=email, ip=ip)
        access_token = Security.create_access_token(user)
        token = TokenResponse(access_token=access_token)
        return BaseResponse[TokenResponse](success=True, data=token)