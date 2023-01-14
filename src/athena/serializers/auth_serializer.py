from pydantic import BaseModel, Field, validator

import regex


class TokenResponseSerializer(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenDataSerializer(BaseModel):
    username: str | None = None


class TokenRequestHeaders(BaseModel):
    access_token: str = Field(..., alias='Authorization')

    @validator('access_token')
    @classmethod
    def clean_authorization_token(cls, value: str) -> str:
        return regex.search(
            r'\baccess_token=\"(?P<token>.+?)\";?',
            value, regex.I | regex.S
        )['token']

    class Config:
        allow_population_by_field_name = True
