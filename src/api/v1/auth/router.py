from fastapi import APIRouter, Depends
from .paths import AuthPaths
from .service import AuthService, get_auth_service
from .schemas import LoginRequest, TokenResponse
from src.core.response import BaseResponse
from src.api.dependencies.guards import AuthGuard
from src.api.dependencies.models import AuthenticatedUser

router = APIRouter()

# return result of dependenciy:
# result = Depends(get_current_user)

# not return result of dependency, just run dependency:
# dependencies=[Depends(get_current_user)]


@router.get(AuthPaths.ME, response_model=BaseResponse[AuthenticatedUser])
def read_me(user : AuthenticatedUser = AuthGuard()):
    return BaseResponse[AuthenticatedUser](data=user)


@router.post(AuthPaths.LOGIN, response_model=BaseResponse[TokenResponse])
def login(credentials: LoginRequest, service: AuthService = Depends(get_auth_service)):
    return service.login(credentials=credentials)