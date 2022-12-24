from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config as conf


config = conf.configuration

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = "{config['db_connection']['driver']}://{config['db_connection']['user']}:{config['db_connection']['password']}@{config['db_connection']['server']}/{config['db_connection']['database']}"

#engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
engine = create_engine(
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    SQLALCHEMY_DATABASE_URL, echo=True
)
print(engine.table_names())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
