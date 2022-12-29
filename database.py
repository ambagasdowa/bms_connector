import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import configuration
config = configuration['db_connection']


SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(config['user'],config['password'],config['server'],config['database'])

#engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
engine = create_engine(
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    SQLALCHEMY_DATABASE_URL, echo=True, encoding='utf8'
)

print(engine.table_names())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
