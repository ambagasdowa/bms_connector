from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib
from .config import configuration


config = configuration['db_connection']

print(config)

params = urllib.parse.quote_plus("".format(config['driver'])
                                 "://".format(config['user'])
                                 ":".format(config['password'])
                                 "@".format(config['server'])
                                 "/".format(config['database']))

#engine = sa.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))


# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = format.(params)
print("THE URL :")
print(SQLALCHEMY_DATABASE_URL)
#engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
engine = create_engine(
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    SQLALCHEMY_DATABASE_URL, echo=True
)
print(engine.table_names())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
