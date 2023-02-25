from fastapi import APIRouter, Depends


from sqlalchemy import select


from extensions.logger import logger

from serializers.user_serializer import UserResponseBody

from .auth_router import async_get_current_user

from ..database.connection import database
from ..database.models.user_model import UserModel

from ..utils.exceptions import NotAuthorizedError


class RoleChecker:
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def __call__(
        self, user: UserModel = Depends(async_get_current_user)
    ):
        if user.role not in self.allowed_roles:
            logger.debug(
                f'User with role {user.role} not in {self.allowed_roles}'
            )
            raise NotAuthorizedError()


router = APIRouter()


@router.get(
    '',
    response_model=list[UserResponseBody],
    dependencies=[Depends(RoleChecker(['admin']))]
)
async def get_users(username: str | None = None):
    if username:
        query = select(UserModel).where(UserModel.username == username)
    else:
        query = select(UserModel)
    return await database.fetch_all(query)
