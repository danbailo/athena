from enum import StrEnum


from sqlalchemy import Boolean, Column, String, Enum
from sqlalchemy.sql import false


from .base import AthenaBase


class RoleEnum(StrEnum):
    admin = 'admin'
    user = 'user'
    superuser = 'superuser'


class UserModel(AthenaBase):
    name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, server_default=false(), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, server_default=RoleEnum.user)
