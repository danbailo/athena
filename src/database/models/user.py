from sqlalchemy import Boolean, Column, String


from .base import AtenaBase


class UserModel(AtenaBase):
    name = Column(String)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_active = Column(Boolean, default=False)
