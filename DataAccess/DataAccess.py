import pymysql
import os
from sqlalchemy import create_engine

from system_config import SystemConfig
import pdb  # debugging tool -- pdb.set_trace()

class DataAccess():

    def __init__(self):
        self.sysConfig = SystemConfig()
        self.Username = self.sysConfig.DATABASE_USERNAME 
        self.Password = self.sysConfig.DATABASE_PASSWORD 
        self.Host = self.sysConfig.DATABASE_HOST 
        self.Port = self.sysConfig.DATABASE_PORT 
        self.Database = self.sysConfig.DATABASE_NAME 

        self.engine = create_engine(
            'mysql+pymysql://' + self.Username + ':' + self.Password + '@' + self.Host + ':' + self.Port + '/' + self.Database
            #,
            #pool_size=10, 
            #max_overflow=20
        )

        self.connection = self.engine.connect()
        self.raw_connection = self.engine.raw_connection()
        self.cursor = self.engine.raw_connection().cursor()
        self.transaction = None
    
    def close_connection(self):
        self.cursor.close()
        self.connection.close()
        self.raw_connection.close()
        self.engine.dispose()

    def begin_transaction(self):
        self.transaction = self.connection.begin()

    def commit_transaction(self):
        self.transaction.commit()

    def rollback_transaction(self):
        self.transaction.rollback()
