from fastapi import APIRouter, Depends, status

from sqlalchemy import select, insert, update


from database.connection import database
from database.models.user import UserModel

from .auth_router import get_current_active_user

from ..serializers.user_serializer import CreateUserSerializer, GetUserSerializer, BaseUserSerializer

from extensions.exceptions import UserNotFound

router = APIRouter()


@router.get('/', response_model=list[GetUserSerializer])
async def get_users():
    query = select(UserModel)
    return await database.fetch_all(query)


@router.post('/', response_model=CreateUserSerializer)
async def create_user(user: CreateUserSerializer):
    query = insert(UserModel).values(**user.dict(by_alias=False))
    await database.execute(query)
    return user


@router.get("/me", response_model=GetUserSerializer)
async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user


@router.get("/me/items/")
async def read_own_items(current_user: UserModel = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
