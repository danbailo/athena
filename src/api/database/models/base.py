from sqlalchemy import Column, BigInteger, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr


import regex


@as_declarative()
class AthenaBase:

    @declared_attr
    def __tablename__(cls):
        if match := regex.search(r'(.+?)model', cls.__name__, flags=regex.I):
            return match.group(1).lower()
        raise ValueError('the table name is not in the default!')

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
