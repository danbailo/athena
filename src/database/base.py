import databases

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base


from extensions.env_var import get_env_var


DATABASE_URL = (
    'postgresql://'
    f'{get_env_var("DB_USER")}:'
    f'{get_env_var("DB_PASSWORD")}@'
    f'{get_env_var("DB_HOST")}/'
    f'{get_env_var("DB_DATABASE")}'
)
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
Base = declarative_base()
