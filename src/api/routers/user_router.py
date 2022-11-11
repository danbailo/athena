from fastapi import APIRouter, Depends, status

from sqlalchemy import select, insert, update


from database.connection import database
from database.models.user import UserModel

from .auth_router import get_current_active_user

from ..serializers.user_serializer import CreateUserBody, GetUserBody, BaseUserBody, PatchUserBody

from extensions.exceptions import UserNotFoundError, NothingToPatchError

router = APIRouter()


@router.get('/', response_model=list[GetUserBody])
async def get_users():
    query = select(UserModel)
    return await database.fetch_all(query)


@router.post('/', response_model=CreateUserBody)
async def create_user(user: CreateUserBody):
    query = insert(UserModel).values(**user.dict(by_alias=False))
    await database.execute(query)
    return user


@router.get("/me", response_model=GetUserBody)
async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user


@router.get("/me/items/")
async def read_own_items(current_user: UserModel = Depends(get_current_active_user)):
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
