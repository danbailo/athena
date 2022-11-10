from pydantic import BaseModel, Field, validator


class BaseUserSerializer(BaseModel):
    name: str
    username: str
    email: str

    class Config:
        allow_population_by_field_name = True


class CreateUserSerializer(BaseUserSerializer):
    password_hash: str = Field(..., alias='password')


class GetUserSerializer(CreateUserSerializer):
    id: int
    is_active: bool | None
