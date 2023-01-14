from pydantic import BaseModel, Field, validator


from api.database.models.user_model import RoleEnum
from api.utils.auth_util import get_password_hash


class BaseUserBody(BaseModel):
    name: str
    username: str
    email: str

    class Config:
        allow_population_by_field_name = True


class CreateUserRequestBody(BaseUserBody):
    password_hash: str = Field(..., alias='password')

    @validator('password_hash')
    @classmethod
    def hash_password(cls, value: str) -> str:
        return get_password_hash(value)


class PatchUserRequestBody(BaseModel):
    name: str | None
    email: str | None
    password_hash: str = Field(..., alias='password')

    @validator('password_hash')
    @classmethod
    def hash_password(cls, value: str) -> str:
        return get_password_hash(value)


class UserResponseBody(BaseUserBody):
    role: RoleEnum
