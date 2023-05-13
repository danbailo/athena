from datetime import datetime


from pydantic import BaseModel, Field, validator


from ares.database.models.user_model import RoleEnum
from ares.utils.auth_util import get_password_hash


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
    password_hash: str | None = Field(None, alias='password')

    @validator('password_hash')
    @classmethod
    def hash_password(cls, value: str) -> str:
        if value:
            return get_password_hash(value)


class UserResponseBody(BaseUserBody):
    id: int
    role: RoleEnum
    created_at: datetime
