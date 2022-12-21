from databases import Database

import sqlalchemy
from sqlalchemy.engine import Engine


from extensions.env_var import get_env_var

# TODO: IMPROVE IT
conn_string = (
    get_env_var('DOCKER_CONN_STRING') or get_env_var('DB_CONN_STRING')
)
DATABASE_URL = f'postgresql://{conn_string}'
database = Database(DATABASE_URL)


def get_engine() -> Engine:
    return sqlalchemy.create_engine(DATABASE_URL)
