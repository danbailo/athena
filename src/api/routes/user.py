from fastapi import APIRouter


from database.connection import database
from database.models.user import UserModel

from ..serializers.user import UserInSerializer, UserOutSerializer

from sqlalchemy import select, insert

router = APIRouter()


@router.get('/', response_model=list[UserOutSerializer])
async def get_users():
    query = select(UserModel)
    return await database.fetch_all(query)


@router.post('/', response_model=UserInSerializer)
async def create_user(user: UserInSerializer):
    query = insert(UserModel).values(**user.dict(by_alias=True))
    await database.execute(query)
    return user
