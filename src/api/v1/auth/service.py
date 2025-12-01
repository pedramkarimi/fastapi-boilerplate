from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.api.v1.user.repository import UserRepository
from .schemas import LoginRequest, TokenResponse
from src.core.response import BaseResponse
from src.core.errors import ErrorMessages
from src.core.security import Security

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def login(self, credentials: LoginRequest) -> BaseResponse[TokenResponse]:
        user = self.user_repo.get_user_by_email(credentials.email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorMessages.INVALID_CREDENTIALS)
        
        password_is_verified = Security.verify_password(credentials.password, user.password)
        if not password_is_verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorMessages.INVALID_CREDENTIALS)
        
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ErrorMessages.USER_IS_INACTIVE)
        
        access_token = Security.create_access_token(user)
        token = TokenResponse(access_token=access_token)
        return BaseResponse[TokenResponse](success=True, data=token)




def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)