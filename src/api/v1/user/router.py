from fastapi import APIRouter, Depends, status
from .service import UserService
from .schemas import UserResponse, UserCreate, UserUpdate
from .paths import UserPaths
from src.core.response import PaginationResponse, BaseResponse
from src.db.session import get_db
from sqlalchemy.orm import Session
from redis.asyncio import Redis
from src.core.redis import get_redis
from .service import UserService

router = APIRouter()

def get_user_service(
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> UserService:
    return UserService(db=db, redis=redis)


@router.get(UserPaths.LIST, response_model=PaginationResponse[UserResponse])
async def users_list(
    skip: int = 0,
    limit: int = 10,
    service: UserService = Depends(get_user_service),
):
    return await service.users_list(skip=skip, limit=limit)


@router.post(UserPaths.CREATE, response_model=BaseResponse[UserResponse], status_code=status.HTTP_201_CREATED)
def user_create(user: UserCreate, service: UserService = Depends(get_user_service)):
    return service.user_create(user=user)


@router.put(UserPaths.UPDATE, response_model=BaseResponse[UserResponse])
def user_update(user_id: int, user : UserUpdate,  service: UserService = Depends(get_user_service)):
    return service.user_update(user_id= user_id, user = user)


@router.delete(UserPaths.DELETE, response_model=BaseResponse[bool])
def user_delete(user_id : int, service: UserService = Depends(get_user_service)):
    return service.user_delete(user_id = user_id)
    

@router.get(UserPaths.GET_ONE, response_model=BaseResponse[UserResponse])
def get_user_by_id(user_id: int, service: UserService=Depends(get_user_service)):
    return service.get_user_by_id(user_id=user_id)