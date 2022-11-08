from pydantic import BaseModel, Field


class UserInSerializer(BaseModel):
    name: str
    username: str
    email: str
    password: str = Field(..., alias='password_hash')

    class Config:
        allow_population_by_field_name = True


class UserOutSerializer(UserInSerializer):
    id: int
