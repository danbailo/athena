from databases import Database

import sqlalchemy
from sqlalchemy.engine import Engine


from extensions.env_var import get_env_var


DATABASE_URL = (
    'postgresql://'
    f'{get_env_var("DB_USER")}:'
    f'{get_env_var("DB_PASSWORD")}@'
    f'{get_env_var("DB_HOST")}/'
    f'{get_env_var("DB_DATABASE")}'
)
database = Database(DATABASE_URL)


def get_engine() -> Engine:
    return sqlalchemy.create_engine(DATABASE_URL)
