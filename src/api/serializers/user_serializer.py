from pydantic import BaseModel, Field, validator


from ..utils.auth_util import get_password_hash


class BaseUserSerializer(BaseModel):
    name: str
    username: str
    email: str

    class Config:
        allow_population_by_field_name = True


class CreateUserSerializer(BaseUserSerializer):
    password_hash: str = Field(..., alias='password')

    @validator('password_hash')
    @classmethod
    def hash_password(cls, value: str) -> str:
        return get_password_hash(value)


class GetUserSerializer(CreateUserSerializer):
    id: int
    is_active: bool | None
