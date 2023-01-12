from pydantic import BaseModel, Field, validator


from api.database.models.user_model import RoleEnum
from api.utils.auth_util import get_password_hash


class BaseUserBody(BaseModel):
    name: str
    username: str
    email: str
    is_active: bool | None
    role: RoleEnum

    class Config:
        allow_population_by_field_name = True


class CreateUserBody(BaseUserBody):
    password_hash: str = Field(..., alias='password')

    @validator('password_hash')
    @classmethod
    def hash_password(cls, value: str) -> str:
        return get_password_hash(value)


class GetUserBody(BaseUserBody):
    id: int


class PatchUserBody(BaseModel):
    name: str | None
    email: str | None
    is_active: bool | None
