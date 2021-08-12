from sqlalchemy import Table, Column, Integer, DateTime, String, Float, MetaData

from DataAccess.DataAccess import DataAccess
from Util.ErrorHandler import InsertError, UpdateError, DeleteError, FetchError

class MeetingInvitation(): 

    def __init__(self, MeetingInvitationId = None, MeetingId = None, AccessGroupId = None,  data_access = None):
        self.meta = MetaData()
        self.data_access = data_access

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsDeleted = False

        self.content = Table(
            'MeetingInvitation', self.meta,
            Column('MeetingInvitationId', Integer, primary_key = True),
            Column('MeetingId', Integer),
            Column('AccessGroupId', Integer),
        )

        self.MeetingInvitationId = MeetingInvitationId
        self.MeetingId = MeetingId
        self.AccessGroupId = AccessGroupId
        
    def Save(self):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_insert_check()
                self._db_insert()
            else:
                self._db_update_check()
                self._db_update()
        except InsertError as insert_error:
            raise insert_error

    def DBFetch(self, MeetingInvitationId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(MeetingInvitationId)
        except FetchError as fetch_error:
            raise fetch_error

    def Delete(self):
        try:
            if self.IsInserted or self.IsFetched:
                self._db_delete_check()
                self._db_delete()
            else:
                raise DeleteError('The MeetingInvitation is neither fetched nor inserted.')
        except DeleteError as delete_error:
            raise delete_error

    def _db_insert_check(self):
        if self.IsDeleted:
            raise InsertError('The MeetingInvitation is deleted.')

        if self.IsInserted:
            raise InsertError('The MeetingInvitation has already been inserted.')

        if self.IsUpdated:
            raise InsertError('The MeetingInvitation has been inserted.')

        if self.MeetingId == None:
            raise InsertError('Please make sure that MeetingId has a value.')

        if self.AccessGroupId == None:
            raise InsertError('Please make sure that AccessGroupId has a value.')

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'MeetingId':self.MeetingId, 'AccessGroupId':self.AccessGroupId},
            ])
            self.MeetingInvitationId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        if self.IsDeleted:
            raise FetchError('The MeetingInvitation is deleted.')

    def _db_fetch(self, MeetingInvitationId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.MeetingInvitationId == MeetingInvitationId)
            result = self.data_access.connection.execute(s)
            row = result.first()

            if row == None:
                raise FetchError('The MeetingInvitation does not exist. MeetingInvitation Id is {0}.'.format(str(MeetingInvitationId)))
            else:
                #Get results and assign them to class variables

                self.MeetingInvitationId = row[0]
                self.MeetingId = row[1]
                self.AccessGroupId = row[2]
                self.IsFetched = True

    def _db_delete_check(self):
        if self.IsDeleted:
            raise DeleteError('The MeetingInvitation is deleted.')

    def _db_delete(self):
        s = self.content.delete().where(self.content.c.MeetingInvitationId == self.MeetingInvitationId)
        self.data_access.connection.execute(s)

        self.IsDeleted = True

    def _db_update_check(self):
        if self.IsDeleted:
            raise UpdateError('The MeetingInvitation is deleted.')

    def _db_update(self):
        s = self.content.update().where(self.content.c.MeetingInvitationId == self.MeetingInvitationId).values(MeetingId = self.MeetingId, AccessGroupId = self.AccessGroupId)
        self.data_access.connection.execute(s)

        self.IsUpdated = True
