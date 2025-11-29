from fastapi import APIRouter, Depends
from .paths import AuthPaths
from .service import AuthService, get_auth_service
from .schemas import LoginRequest, TokenResponse
from src.core.response import BaseResponse

router = APIRouter()

@router.post(AuthPaths.LOGIN, response_model=BaseResponse[TokenResponse])
def login(credentials: LoginRequest, service: AuthService = Depends(get_auth_service)):
    return service.login(credentials=credentials)