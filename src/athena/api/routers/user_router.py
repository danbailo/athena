from fastapi import APIRouter, Depends, status

from sqlalchemy import select, insert, update


from extensions.exceptions import (
    NotAuthorizedError, NothingToPatchError, UserNotFoundError
)
from extensions.logger import logger

from serializers.user_serializer import (
    CreateUserBody, GetUserBody, PatchUserBody
)

from .auth_router import async_get_current_active_user

from ..database.connection import database
from ..database.models.user_model import UserModel


router = APIRouter()


class RoleChecker:
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def __call__(
        self, user: UserModel = Depends(async_get_current_active_user)
    ):
        if user.role not in self.allowed_roles:
            logger.debug(
                f'User with role {user.role} not in {self.allowed_roles}'
            )
            raise NotAuthorizedError()


@router.get('', response_model=list[GetUserBody])
async def get_users(username: str | None = None):
    if username:
        query = select(UserModel).where(UserModel.username == username)
    else:
        query = select(UserModel)
    return await database.fetch_all(query)


@router.post('', response_model=CreateUserBody)
async def create_user(user: CreateUserBody):
    query = insert(UserModel).values(**user.dict(by_alias=False))
    await database.execute(query)
    return user


@router.get("/me", response_model=GetUserBody)
async def read_users_me(
    current_user: UserModel = Depends(async_get_current_active_user)
):
    return current_user


@router.get("/me/items/")
async def read_own_items(
    current_user: UserModel = Depends(async_get_current_active_user)
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@router.patch('/{username}', status_code=status.HTTP_204_NO_CONTENT)
async def patch_user(username: str, user_body: PatchUserBody):
    query = select(UserModel).where(UserModel.username == username)
    if not (user := await database.fetch_one(query)):
        raise UserNotFoundError()
    data = user_body.dict(exclude_none=True)
    if not data:
        raise NothingToPatchError()
    query = update(UserModel)\
        .where(UserModel.id == user.id)\
        .values(**data)
    await database.execute(query)


@router.get('/admin', dependencies=[Depends(RoleChecker(['admin']))])
async def only_admin(user: UserModel = Depends(async_get_current_active_user)):
    return {'message': f'{user.name} is admin!'}
