
from fastapi import Depends
from src.api.dependencies.deps import get_current_user_data
from src.api.dependencies.models import AuthenticatedUser

def AuthGuard() -> AuthenticatedUser:
    def wrapper(current_user = Depends(get_current_user_data)) -> AuthenticatedUser:
        return AuthenticatedUser(
            id=current_user.id,
            email=current_user.email
        )
    return Depends(wrapper)