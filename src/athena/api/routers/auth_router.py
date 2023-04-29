from datetime import datetime, timedelta

from typing import Annotated


from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from databases import Database

from jose import JWTError, jwt

from sqlalchemy import select


from constants.mapped_api_prefix import MAPPED_API_ENDPOINT_PREFIX

from extensions.env_var import get_env_var

from serializers.auth_serializer import TokenResponseBody

from ..database.connection import database
from ..database.models.user_model import UserModel

from ..utils.auth_util import verify_password
from ..utils.exceptions import GetUserError, LoginError

SECRET_KEY = get_env_var('SECRET_KEY')
ALGORITHM = get_env_var('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f'{MAPPED_API_ENDPOINT_PREFIX["auth"]}/token'
)


async def async_get_user_in_db(
    db: Database, username: str
) -> UserModel | None:
    query = select(UserModel).where(UserModel.username == username)
    return await db.fetch_one(query)


async def async_get_current_user(
    token: str = Depends(oauth2_scheme)
) -> UserModel:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise GetUserError()
    except JWTError:
        raise GetUserError()

    if not (user := await async_get_user_in_db(database, username)):
        raise GetUserError()
    return user

CurrentUser = Annotated[UserModel, Depends(async_get_current_user)]


async def async_authenticate_user(
    db: Database, username: str, password: str
) -> UserModel | None:
    if not (user := await async_get_user_in_db(db, username))\
       or not verify_password(password, user.password_hash):
        return None
    return user


def create_access_token(
    data: dict, expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/token', response_model=TokenResponseBody)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> TokenResponseBody:
    if not (user := await async_authenticate_user(
        database, form_data.username, form_data.password)
    ):
        raise LoginError()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}
