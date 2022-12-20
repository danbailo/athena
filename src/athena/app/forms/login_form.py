from fastapi import Form

from pydantic import BaseModel, Field


class LoginForm(BaseModel):
    """Is mandatory to return this fields.

    OAuth2PasswordRequestForm
        * grant_type
        * username
        * password
        * scopes
        * client_id
        * client_secret
    """

    username: str = Field(..., alias='username')
    password: str = Field(..., alias='password')
    remember_me: bool

    @classmethod
    def as_form(
        cls,
        username: str = Form(),
        password: str = Form(),
        remember_me: bool = Form(False)
    ) -> 'LoginForm':
        return cls(
            username=username, password=password, remember_me=remember_me
        )

    class Config:
        allow_population_by_field_name = True
