from sqlalchemy import Column, BigInteger, DateTime, and_, select
from sqlalchemy.sql import expression
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.compiler import compiles

import regex


class utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kwargs):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


@as_declarative()
class AthenaBase:

    @declared_attr
    @classmethod
    def __tablename__(cls):
        if match := regex.search(r'(.+?)model', cls.__name__, flags=regex.I):
            return match.group(1).lower()
        raise ValueError('the table name is not in the default!')

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(), server_default=utcnow())


def select_database(
    model: type[AthenaBase],
    query_params: list[dict[str, any]] | None = None,
    page: int = 1,
    limit: int = 30
):
    """select onde sempre compara igualdade"""
    offset = (page-1) * limit
    # last_page = ceil(total/limit)
    if query_params is None:
        query_params = []
    filter_args = [
        getattr(model, key) == value for param in query_params
        for key, value in param.items()
        if (getattr(model, key, None) is not None and value is not None)
    ]
    if filter_args:
        return select(model).where(and_(*filter_args))\
                            .offset(offset).limit(limit)
    return select(model).offset(offset).limit(limit)
