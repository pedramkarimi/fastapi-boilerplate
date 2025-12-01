from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from jose import jwt, JWTError
from src.core.config import settings
from src.api.v1.user.models import User as user_model

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Security:

    def hash_password(password: str) -> str:
        return _pwd_context.hash(password)


    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return _pwd_context.verify(plain_password, hashed_password)


    def create_access_token(user: user_model, expires_delta: Optional[timedelta] = None) -> str:
        now = datetime.now(timezone.utc)
        
        if expires_delta is None:
            expires_delta = timedelta(hours=settings.JWT_ACCESS_TOKEN_EXPIRE_HOURS)
        
        expire = now + expires_delta

        payload = {
        "sub": str(user.id),
        "email": user.email,
        "role": "user",
        "permissions": [],  
        "exp": expire,
        "iat": now,
            }
        
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


    def decode_access_token(token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )