from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy import insert, update
from asyncpg.exceptions import UniqueViolationError


from serializers.user_serializer import (
    CreateUserRequestBody, UserResponseBody, PatchUserRequestBody
)

from .auth_router import async_get_current_user

from ..database.connection import database
from ..database.models.user_model import UserModel

from ..utils.exceptions import NothingToPatchError

router = APIRouter()


@router.post('/detail', response_model=UserResponseBody)
async def user_detail(
    current_user: UserModel = Depends(async_get_current_user)
):
    return current_user


@router.post('', response_model=CreateUserRequestBody)
async def create_user(user: CreateUserRequestBody):
    query = insert(UserModel).values(**user.dict(by_alias=False))
    try:
        await database.execute(query)
    except UniqueViolationError as err:
        msg = "The {field} - {value} is already in use!"
        if 'username' in str(err):
            msg = msg.format(value=user.username, field='username')
        if 'email' in str(err):
            msg = msg.format(value=user.email, field='email')
        raise HTTPException(status_code=400, detail=msg)
    return user


@router.patch('', status_code=status.HTTP_204_NO_CONTENT)
async def update_own_info(
    user_body: PatchUserRequestBody,
    user: UserModel = Depends(async_get_current_user),
):
    data = user_body.dict(exclude_none=True)
    if not data:
        raise NothingToPatchError()
    query = update(UserModel)\
        .where(UserModel.id == user.id)\
        .values(**data)
    await database.execute(query)
