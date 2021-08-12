from sqlalchemy import Table, Column, Integer, String, Float, DateTime, MetaData

from DataAccess.DataAccess import DataAccess

import datetime


class Lists(object):
    def __init__(self):
        pass

    def Users(self):
        users = []
        meta = MetaData()
        data_access = DataAccess()

        content = Table(
            'User', meta,
            Column('UserId', Integer, primary_key=True),
            Column('Firstname', String),
            Column('Lastname', String),
            )

        s = content.select()
        result = data_access.connection.execute(s)

        for row in result: users.append(row)

        data_access.close_connection()

        return users

    def FutureMeetings(self):
        meetings = []
        meta = MetaData()
        data_access = DataAccess()

        content = Table(
            'Meeting', meta,
            Column('MeetingId', Integer, primary_key=True),
            Column('MeetingTypeId', Integer),
            Column('LocationId', Integer),
            Column('Title', String),
            Column('StartDate', DateTime),
            Column('EndDate', DateTime),
            )

        s = content.select().where(content.c.StartDate >= datetime.datetime.now())
        result = data_access.connection.execute(s)

        for row in result: meetings.append(row)

        data_access.close_connection()

        return meetings

    def PastMeetings(self):
        meetings = []
        meta = MetaData()
        data_access = DataAccess()

        content = Table(
            'Meeting', meta,
            Column('MeetingId', Integer, primary_key=True),
            Column('MeetingTypeId', Integer),
            Column('LocationId', Integer),
            Column('Title', String),
            Column('StartDate', DateTime),
            Column('EndDate', DateTime),
            )

        s = content.select().where(content.c.StartDate < datetime.datetime.now())
        result = data_access.connection.execute(s)

        for row in result: meetings.append(row)

        data_access.close_connection()

        return meetings

    def userAccessGroup(self, userId):
        userAccessGroup = []
        meta = MetaData()
        data_access = DataAccess()

        content = Table(
            'UserAccessGroup', meta,
            Column('UserAccessGroupId', Integer, primary_key=True),
            Column('UserId', Integer),
            Column('AccessGroupId', Integer),
            )

        s = content.select().where(content.c.UserId == userId)
        result = data_access.connection.execute(s)

        for row in result: userAccessGroup.append(row)

        data_access.close_connection()

        return userAccessGroup

    def fileAccess(self, fileId):
        fileAccess = []
        meta = MetaData()
        data_access = DataAccess()

        content = Table(
            'FileAccess', meta,
            Column('FileAccessId', Integer, primary_key=True),
            Column('FileId', Integer),
            Column('AccessGroupId', Integer),
            )

        s = content.select().where(content.c.FileId == fileId)
        result = data_access.connection.execute(s)

        for row in result: fileAccess.append(row)

        data_access.close_connection()

        return fileAccess

    def meetingFile(self, fileId):
        meetingFile = []
        meta = MetaData()
        data_access = DataAccess()

        content = Table(
            'MeetingFile', meta,
            Column('MeetingFileId', Integer, primary_key=True),
            Column('MeetingId', Integer),
            Column('FileId', Integer),
        )

        s = content.select().where(content.c.FileId == fileId)
        result = data_access.connection.execute(s)

        for row in result: meetingFile.append(row)

        data_access.close_connection()

        return meetingFile

    def meetingInvitations(self, meetingId):
        meetingInvitations = []
        meta = MetaData()
        data_access = DataAccess()

        content = Table(
            'MeetingInvitation', meta,
            Column('MeetingInvitationId', Integer, primary_key=True),
            Column('MeetingId', Integer),
            Column('AccessGroupId', Integer),
        )

        s = content.select().where(content.c.MeetingId == meetingId)
        result = data_access.connection.execute(s)

        for row in result: meetingInvitations.append(row)

        data_access.close_connection()

        return meetingInvitations
