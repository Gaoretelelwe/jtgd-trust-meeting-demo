from sqlalchemy import Table, Column, Integer, DateTime, String, MetaData

from Util.ErrorHandler import InsertError, UpdateError, DeleteError, FetchError
import pdb  # debugging tool -- pdb.set_trace()

class Session(): 

    def __init__(self, SessionId = None, SessionGuid = None, CreateDate = None, LastAccessDate = None, UniqueAccessDays = 0, UserId = None, AdminInd = 0, LoggedInInd = 0, RememberInd = 0, MemberId = None, LoggedinEntityName = None, data_access = None):
        self.meta = MetaData()
        self.data_access = data_access

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsDeleted = False

        self.content = Table(
            'Session', self.meta,
            Column('SessionId', Integer, primary_key=True),
            Column('SessionGuid', String),
            Column('CreateDate', DateTime),
            Column('LastAccessDate', DateTime),
            Column('UniqueAccessDays', Integer),
            Column('UserId', Integer),
            Column('AdminInd', Integer),
            Column('LoggedInInd', Integer),
            Column('RememberInd', Integer),
            Column('MemberId', Integer),
            Column('LoggedinEntityName', String),
        )

        self.SessionId = SessionId
        self.SessionGuid = SessionGuid
        self.CreateDate = CreateDate
        self.LastAccessDate = LastAccessDate
        self.UniqueAccessDays = UniqueAccessDays
        self.UserId = UserId
        self.AdminInd = AdminInd
        self.LoggedInInd = LoggedInInd
        self.RememberInd = RememberInd
        self.MemberId = MemberId
        self.LoggedinEntityName = LoggedinEntityName
        
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

    def DBFetch(self, SessionId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(SessionId)
        except FetchError as fetch_error:
            raise fetch_error

    def DBFetchGUID(self, SessionGuid):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch_guid(SessionGuid)
        except FetchError as fetch_error:
            raise fetch_error

    def Delete(self):
        try:
            if self.IsInserted or self.IsFetched:
                self._db_delete_check()
                self._db_delete()
            else:
                raise DeleteError('The Session is neither fetched nor inserted.')
        except DeleteError as delete_error:
            raise delete_error

    def _db_insert_check(self):
        if self.IsDeleted:
            raise InsertError('The Session is deleted.')

        if self.IsInserted:
            raise InsertError('The Session has already been inserted.')

        if self.IsUpdated:
            raise InsertError('The Session has been inserted.')

        if self.SessionGuid == None:
            raise InsertError('Please make sure that SessionGuid has a value.')

        if self.CreateDate == None:
            raise InsertError('Please make sure that CreateDate has a value.')

        if self.LastAccessDate == None:
            raise InsertError('Please make sure that LastAccessDate has a value.')

        if self.UniqueAccessDays == None:
            raise InsertError('Please make sure that UniqueAccessDays has a value.')

        if self.AdminInd == None:
            raise InsertError('Please make sure that AdminInd has a value.')

        if self.LoggedInInd == None:
            raise InsertError('Please make sure that LoggedInInd has a value.')

        if self.RememberInd == None:
            raise InsertError('Please make sure that RememberInd has a value.')

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'SessionGuid':self.SessionGuid, 'CreateDate':self.CreateDate, 'LastAccessDate':self.LastAccessDate, 'UniqueAccessDays':self.UniqueAccessDays, 'UserId':self.UserId, 'AdminInd':self.AdminInd, 'LoggedInInd':self.LoggedInInd, 'RememberInd':self.RememberInd, 'MemberId':self.MemberId, 'LoggedinEntityName':self.LoggedinEntityName},
            ])
            self.SessionId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        if self.IsDeleted:
            raise FetchError('The Session is deleted.')

    def _db_fetch(self, SessionId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.SessionId == SessionId)
            result = self.data_access.connection.execute(s)
            row = result.first()

            if row == None:
                raise FetchError('The Session does not exist. Session Id is {0}.'.format(str(SessionId)))
            else:
                #Get results and assign them to class variables

                self.SessionId = row[0]
                self.SessionGuid = row[1]
                self.CreateDate = row[2]
                self.LastAccessDate = row[3]
                self.UniqueAccessDays = row[4]
                self.UserId = row[5]
                self.AdminInd = row[6]
                self.LoggedInInd = row[7]
                self.RememberInd = row[8]
                self.MemberId = row[9]
                self.LoggedinEntityName = row[10]
                self.IsFetched = True

    def _db_fetch_guid(self, SessionGuid):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.SessionGuid == SessionGuid)
            result = self.data_access.connection.execute(s)
            row = result.first()

            if row == None:
                raise FetchError('The Session does not exist. Session Guid is {0}.'.format(str(SessionGuid)))
            else:
                #Get results and assign them to class variables

                self.SessionId = row[0]
                self.SessionGuid = row[1]
                self.CreateDate = row[2]
                self.LastAccessDate = row[3]
                self.UniqueAccessDays = row[4]
                self.UserId = row[5]
                self.AdminInd = row[6]
                self.LoggedInInd = row[7]
                self.RememberInd = row[8]
                self.MemberId = row[9]
                self.LoggedinEntityName = row[10]
                self.IsFetched = True

    def _db_delete_check(self):
        if self.IsDeleted:
            raise DeleteError('The Session is deleted.')

    def _db_delete(self):
        s = self.content.delete().where(self.content.c.SessionId == self.SessionId)
        self.data_access.connection.execute(s)

        self.IsDeleted = True

    def _db_update_check(self):
        if self.IsDeleted:
            raise UpdateError('The Session is deleted.')

    def _db_update(self):
        s = self.content.update().where(self.content.c.SessionId == self.SessionId).values(SessionGuid = self.SessionGuid, CreateDate = self.CreateDate, LastAccessDate = self.LastAccessDate, UniqueAccessDays = self.UniqueAccessDays, UserId = self.UserId, AdminInd = self.AdminInd, LoggedInInd = self.LoggedInInd, RememberInd = self.RememberInd, MemberId = self.MemberId, LoggedinEntityName = self.LoggedinEntityName)
        self.data_access.connection.execute(s)

        self.IsUpdated = True
