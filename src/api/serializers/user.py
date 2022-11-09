from pydantic import BaseModel, Field


class CreateUserSerializer(BaseModel):
    name: str
    username: str
    email: str
    password_hash: str = Field(..., alias='password')

    class Config:
        allow_population_by_field_name = True


class GetUserSerializer(CreateUserSerializer):
    id: int
