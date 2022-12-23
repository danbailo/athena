from pydantic import BaseModel


class TokenResponseSerializer(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenDataSerializer(BaseModel):
    username: str | None = None
