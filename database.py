import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import configuration
config = configuration['db_connection']

## set your parameters for the database
#user = "user"
#password = "password"
#host = "abc.efg.hij.rds.amazonaws.com"
#port = 3306
#schema = "db_schema"
# 
## Connect to the database
#conn_str = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8mb4'.format(
#    user, password, host, port, schema)
#db = create_engine(conn_str, encoding='utf8')
#connection = db.raw_connection()
# 
## define parameters to be passed in and out
#parameterIn = 1
#parameterOut = "@parameterOut"
#try:
#    cursor = connection.cursor()
#    cursor.callproc("storedProcedure", [parameterIn, parameterOut])
#    # fetch result parameters
#    results = list(cursor.fetchall())
#    cursor.close()
#    connection.commit()
#finally:
#    connection.close() 

#SQLALCHEMY_DATABASE_URL = "mysql+pymysql://ambagasdowa:pekas@127.0.0.1/db_ediq2021"
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(config['user'],config['password'],config['server'],config['database'])

#engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
engine = create_engine(
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    SQLALCHEMY_DATABASE_URL, echo=True, encoding='utf8'
)
#connection = engine.raw_connection()

print(engine.table_names())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
