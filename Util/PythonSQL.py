from Util.ErrorHandler import InsertError, UpdateError, DeleteError, FetchError, LoginError

from sqlalchemy import Table, Column, Integer, String, Float, MetaData, and_
from DataAccess.DataAccess import DataAccess

from Objects.DataObjects.DatabaseObjects import AccessGroup, File, Location, Meeting, MeetingAccess, MeetingInvitation, MeetingType, User, UserAccessGroup
from Objects.DataObjects.Session import Session

class PythonSQL(object):
    def __init__(self):
        pass

    def getAccessGroupByName(self, name, data_access):
        self.meta = MetaData()
        self.data_access = data_access

        self.content = Table(
            'AccessGroup', self.meta,
            Column('AccessGroupId', Integer, primary_key = True),
            Column('Name', String),
        )

        s = self.content.select().where(self.content.c.Name == name)
        result = self.data_access.connection.execute(s)
        row = result.first()

        if row == None:
            return None
        else:
            self.AccessGroupId = row[0]
            self.Name = row[1]

            accessGroup = AccessGroup(self.AccessGroupId, self.Name, self.data_access)
            accessGroup.IsFetched = True
            
            return accessGroup
    
    def getUserAccessGroup(self, UserId, AccessGroupId, data_access):
        self.meta = MetaData()
        self.data_access = data_access

        self.content = Table(
            'UserAccessGroup', self.meta,
            Column('UserAccessGroupId', Integer, primary_key = True),
            Column('UserId', Integer),
            Column('AccessGroupId', Integer),
        )

        s = self.content.select().where(and_(self.content.c.UserId == UserId,
                                             self.content.c.AccessGroupId == AccessGroupId))
        result = self.data_access.connection.execute(s)
        row = result.first()

        if row == None:
            return None
        else:
            self.UserAccessGroupId = row[0]
            self.UserId = row[1]
            self.AccessGroupId = row[2]

            userAccessGroup = UserAccessGroup(UserAccessGroupId=self.UserAccessGroupId, UserId=self.UserId, AccessGroupId=self.AccessGroupId, data_access=self.data_access)
            userAccessGroup.IsFetched = True
            
            return userAccessGroup
    
    def getMeetingInvitation(self, MeetingId, AccessGroupId, data_access):
        self.meta = MetaData()
        self.data_access = data_access

        self.content = Table(
            'MeetingInvitation', self.meta,
            Column('MeetingInvitationId', Integer, primary_key = True),
            Column('MeetingId', Integer),
            Column('AccessGroupId', Integer),
        )

        s = self.content.select().where(and_(self.content.c.MeetingId == MeetingId,
                                             self.content.c.AccessGroupId == AccessGroupId))
        result = self.data_access.connection.execute(s)
        row = result.first()

        if row == None:
            return None
        else:
            self.MeetingInvitationId = row[0]
            self.MeetingId = row[1]
            self.AccessGroupId = row[2]

            meetingInvitation = MeetingInvitation(MeetingInvitationId=self.MeetingInvitationId, MeetingId=self.MeetingId, AccessGroupId=self.AccessGroupId, data_access=self.data_access)
            meetingInvitation.IsFetched = True
            
            return meetingInvitation

    def getUserAccessGroups(self, accessGroupId, data_access):
        userAccessGroups = []
        meta = MetaData()

        content = Table(
            'UserAccessGroup', meta,
            Column('UserAccessGroupId', Integer, primary_key = True),
            Column('UserId', Integer),
            Column('AccessGroupId', Integer),
        )

        s = content.select().where(content.c.AccessGroupId == accessGroupId)
        result = data_access.connection.execute(s)

        for row in result:
            userAccessGroups.append(row)

        return userAccessGroups
