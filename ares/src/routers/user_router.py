from fastapi import APIRouter, status, HTTPException

from sqlalchemy import insert, update
from asyncpg.exceptions import UniqueViolationError


from serializers.user_serializer import (
    CreateUserRequestBody, UserResponseBody, PatchUserRequestBody
)

from .auth_router import CurrentUser

from database.connection import database
from database.models.user_model import UserModel

from utils.exceptions import NothingToPatchError

router = APIRouter()


@router.post('/detail', response_model=UserResponseBody)
async def user_detail(current_user: CurrentUser):
    return current_user


@router.post('', response_model=CreateUserRequestBody)
async def create_user(user: CreateUserRequestBody):
    query = insert(UserModel).values(**user.dict(by_alias=False))
    try:
        await database.execute(query)
    except UniqueViolationError as exc:
        msg = 'O {field} "{value}" já está sendo utilizado!'
        if 'username' in str(exc):
            msg = msg.format(value=user.username, field='username')
        if 'email' in str(exc):
            msg = msg.format(value=user.email, field='email')
        raise HTTPException(status_code=400, detail=msg) from exc
    return user


@router.patch('', status_code=status.HTTP_204_NO_CONTENT)
async def update_own_info(
    user_body: PatchUserRequestBody,
    user: CurrentUser,
):
    data = user_body.dict(exclude_none=True)
    if not data:
        raise NothingToPatchError()
    query = update(UserModel)\
        .where(UserModel.id == user.id)\
        .values(**data)
    await database.execute(query)
