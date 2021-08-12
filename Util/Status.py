
from sqlalchemy import Table, Column, Integer, DateTime, String, MetaData

from DataAccess.DataAccess import DataAccess
from Util.ErrorHandler import InsertError, UpdateError, DeleteError, FetchError

class Status():
    def __init__(self):
        pass
    
    def get_Registration_StatusId(self, StatusType, StatusName):
        data_access = DataAccess
        meta = MetaData()
        data_access = DataAccess()

        status_type_content = Table(
            'StatusType', meta,
            Column('StatusTypeId', Integer, primary_key = True), 
            Column('Name', String), 
        )

        system_status_content = Table(
            'SystemStatus', meta,
            Column('SystemStatusId', Integer, primary_key = True), 
            Column('StatusTypeId', Integer), 
            Column('Name', String), 
        )