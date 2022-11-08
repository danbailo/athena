from sqlalchemy import Boolean, Column, Integer, String


from .base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String)
    password_hash = Column(String)
    is_active = Column(Boolean, default=False)

    def __init__(self, **kwargs):
        self.email = kwargs.get('email')
        self.username = kwargs.get('username')
        self.name = kwargs.get('name')
        self.password_hash = kwargs.get('password_hash')
        self.is_active = kwargs.get('is_active')
