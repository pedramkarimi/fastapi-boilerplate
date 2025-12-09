from fastapi import Depends
from src.db.session import get_db
from sqlalchemy.orm import Session
from .schemas import UserCreate, UserResponse, to_user_response, UserUpdate
from .repository import UserRepository
from src.core.security import Security
from src.core.errors import ErrorMessages
from src.core.response import PaginationResponse, BaseResponse
from src.core.exceptions import ConflictException, ValidationException, NotFoundException
from src.core.redis_keys import RedisKeys
from src.core.cache.base import get_or_set
from src.core.config import settings
from redis.asyncio import Redis
from src.core.cache.decorators import cacheable
from src.messaging.rabbitmq.publishers import publish_welcome_email
from src.messaging.rabbitmq.schemas import WelcomeEmailMessage

class UserService:
    def __init__(self, db: Session, redis: Redis):
        self.db = db
        self.redis = redis
        self.user_repo = UserRepository(db)

    def user_create(self, user: UserCreate) -> UserResponse:
        email_existing = self.user_repo.get_user_by_email(user.email)
        if email_existing:
            raise ConflictException(ErrorMessages.USER_EMAIL_EXISTS)

        password_hash = Security.hash_password(user.password)

        new_user = self.user_repo.user_create(user=user, password_hash=password_hash)

        payload : WelcomeEmailMessage = WelcomeEmailMessage(user_id=new_user.id,email=new_user.email,name=new_user.name)
        publish_welcome_email(payload)

        user_response = to_user_response(new_user)
        return BaseResponse[UserResponse](success=True, data=user_response)

    @cacheable(
        ttl=settings.CACHED_DATA_TTL,
        key_builder=lambda self, skip, limit: RedisKeys.users_list(skip, limit),
        model_cls=PaginationResponse[UserResponse],
    )
    async def users_list(self, skip: int, limit: int) -> list[UserResponse]:
            users = await self.user_repo.users_list(skip=skip, limit=limit)
            total = await self.user_repo.users_count()
            items = [to_user_response(u) for u in users]
            return PaginationResponse[UserResponse](total=total, items=items)
        
    def user_update(self, user_id: int, user: dict) -> BaseResponse[UserResponse]:
        if (user.password is None and user.first_name is None and user.last_name is None):
            raise ValidationException(detail=ErrorMessages.NO_CHANGES_DETECTED)

        db_user = self.user_repo.get_user_by_id(user_id)
        if db_user is None:
            raise NotFoundException(ErrorMessages.USER_NOT_FOUND)
        
        user_new_data = UserUpdate()

        if user.password is not None:
            password_is_verified = Security.verify_password(user.password, db_user.password)
            if not password_is_verified:
                user_new_data.password = Security.hash_password(user.password)
            
        if user.first_name is not None and user.first_name != db_user.name:
            user_new_data.first_name = user.first_name

        if user.last_name is not None and user.last_name != db_user.family:
            user_new_data.last_name = user.last_name
        
        if not user_new_data.model_dump(exclude_none=True):
            raise ValidationException(detail=ErrorMessages.NO_CHANGES_DETECTED)
        
        user_update_data = user_new_data.model_dump(exclude_none=True)
        updated_user = self.user_repo.user_update(db_user=db_user, fields=user_update_data)

        user_response = to_user_response(updated_user)
        return BaseResponse[UserResponse](success=True, data=user_response)

    def user_delete(self, user_id: int) -> BaseResponse[bool]:
        db_user = self.user_repo.get_user_by_id(user_id=user_id)
        if db_user is None:
            raise NotFoundException(ErrorMessages.USER_NOT_FOUND)
        
        deleted_user = self.user_repo.user_delete(db_user)
        print(deleted_user)
        return BaseResponse[bool](
            success=True,
            data=True,
    )

    def get_user_by_id(self, user_id: int):
        db_user = self.user_repo.get_user_by_id(user_id=user_id)
        if db_user is None:
            raise NotFoundException(ErrorMessages.USER_NOT_FOUND)
        
        user = to_user_response(db_user)
        return BaseResponse[UserResponse](success=True, data=user)
