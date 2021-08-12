from sqlalchemy import Table, Column, Integer, String, MetaData

from DataAccess.DataAccess import DataAccess

from Util.StoredProcs import StoredProcs

import datetime

import pdb #debugging tool # pdb.set_trace()

class FormField(object):
    def __init__(self):
        self.default_option = (-100, '')
        self.all_option = (-200, 'ALL')
    
    def get_MeetingTypes(self):
        meetingTypes = [self.default_option]
        meta = MetaData()
        data_access = DataAccess()

        content = Table(
            'MeetingType', meta,
            Column('MeetingTypeId', Integer, primary_key = True), 
            Column('Name', String), 
        )

        s = content.select()  
        result = data_access.connection.execute(s)

        for row in result:
            meetingTypes.append(row)

        data_access.close_connection()

        return meetingTypes
