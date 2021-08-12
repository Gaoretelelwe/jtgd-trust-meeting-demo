from Util.ErrorHandler import InsertError, UpdateError, DeleteError, FetchError, LoginError

from sqlalchemy import Table, Column, Integer, String, Float, MetaData, and_
from DataAccess.DataAccess import DataAccess

from Objects.DataObjects.DatabaseObjects import AccessGroup, File, Location, Meeting, MeetingAccess, MeetingType, User, UserAccessGroup
from Objects.DataObjects.Session import Session

class StoredProcs(object):
    def __init__(self):
        pass
    
    def isAdminUser(self, userId, data_access):
        cursor = data_access.raw_connection.cursor()
        cursor.callproc("getAdminAccessByUserId", [userId])
        result = cursor.fetchall()
        cursor.close()
        
        if result == None: return False
        elif len(result) == 0: return False
        else: return True

        return False

    def getInvitedActiveMeetings(self, userId, data_access):
        cursor = data_access.raw_connection.cursor()
        cursor.callproc("getInvitedActiveMeetings", [userId])
        #result = list(cursor.fetchall())
        result = cursor.fetchall()
        cursor.close()

        meetings = []

        for row in result:
            meeting = Meeting(MeetingId=row[0], data_access=data_access)
            meeting.DBFetch(row[0])
            meetings.append(meeting)

        return meetings

    def getInvitedPastMeetings(self, userId, data_access):
        cursor = data_access.raw_connection.cursor()
        cursor.callproc("getInvitedPastMeetings", [userId])
        #result = list(cursor.fetchall())
        result = cursor.fetchall()
        cursor.close()

        meetings = []

        for row in result:
            meeting = Meeting(MeetingId=row[0], data_access=data_access)
            meeting.DBFetch(row[0])
            meetings.append(meeting)

        return meetings

    def getPermittedFiles(self, userId, meetingId, data_access):
        cursor = data_access.raw_connection.cursor()
        cursor.callproc("getPermittedFiles", [userId, meetingId])
        #result = list(cursor.fetchall())
        result = cursor.fetchall()
        cursor.close()

        permittedFiles = []

        for row in result:
            permittedFiles.append(row)

        return permittedFiles

    def getUserByPasswordRecovery(self, passwordRecovery, data_access):
        cursor = data_access.raw_connection.cursor()
        cursor.callproc("getUserByPasswordRecovery", [passwordRecovery])
        result = cursor.fetchall()
        cursor.close()
        
        if result == None: 
            return None
        elif len(result) == 0:
            return None
        else:
            userId = result[0][0]
            user = User(UserId=userId, data_access=data_access)
            user.DBFetch(user.UserId)

            return user

    def deleteFile(self, fileId, data_access):
        cursor = data_access.raw_connection.cursor()
        cursor.callproc("deleteFile", [fileId])
        result = cursor.fetchall()
        cursor.close()
