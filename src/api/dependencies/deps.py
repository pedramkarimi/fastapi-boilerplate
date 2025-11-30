# src/api/v1/auth/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.core.security import Security
from src.api.v1.user.repository import UserRepository
from src.api.v1.user import models as user_models
from types import SimpleNamespace

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")  

def get_current_user_data(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> user_models.User:
    from jose import JWTError
    try:
        token_data = Security.decode_access_token(token)
        sub = token_data.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    repo = UserRepository(db)
    user = repo.get_user_by_id(int(sub))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return user