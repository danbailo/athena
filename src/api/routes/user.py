from fastapi import APIRouter

from sqlalchemy import select, insert


from database.connection import database
from database.models.user import UserModel

from ..serializers.user import CreateUserSerializer, GetUserSerializer

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
