from databases import Database

import sqlalchemy
from sqlalchemy.engine import Engine


from extensions.env_var import get_env_var

DATABASE_URL = (
    f'postgresql://{get_env_var("DATABASE_CONN_STRING", raise_exception=True)}'
)
database = Database(DATABASE_URL)


def get_engine() -> Engine:
    return sqlalchemy.create_engine(DATABASE_URL)
