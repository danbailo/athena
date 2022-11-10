from sqlalchemy import Boolean, Column, String
from sqlalchemy.sql import false

from .base import AtenaBase


class UserModel(AtenaBase):
    name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, server_default=false(), nullable=False)
