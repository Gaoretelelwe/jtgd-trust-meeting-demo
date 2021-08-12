from sqlalchemy import Table, Column, Integer, DateTime, String, Float, MetaData

from DataAccess.DataAccess import DataAccess
from Util.ErrorHandler import InsertError, UpdateError, DeleteError, FetchError

class AccessGroup(): 

    def __init__(self, AccessGroupId = None, Name = None,  data_access = None):
        self.meta = MetaData()
        self.data_access = data_access

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsDeleted = False

        self.content = Table(
            'AccessGroup', self.meta,
            Column('AccessGroupId', Integer, primary_key = True),
            Column('Name', String),
        )

        self.AccessGroupId = AccessGroupId
        self.Name = Name
        
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

    def DBFetch(self, AccessGroupId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(AccessGroupId)
        except FetchError as fetch_error:
            raise fetch_error

    def Delete(self):
        try:
            if self.IsInserted or self.IsFetched:
                self._db_delete_check()
                self._db_delete()
            else:
                raise DeleteError('The AccessGroup is neither fetched nor inserted.')
        except DeleteError as delete_error:
            raise delete_error

    def _db_insert_check(self):
        if self.IsDeleted:
            raise InsertError('The AccessGroup is deleted.')

        if self.IsInserted:
            raise InsertError('The AccessGroup has already been inserted.')

        if self.IsUpdated:
            raise InsertError('The AccessGroup has been inserted.')

        if self.Name == None:
            raise InsertError('Please make sure that Name has a value.')

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'Name':self.Name},
            ])
            self.AccessGroupId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        if self.IsDeleted:
            raise FetchError('The AccessGroup is deleted.')

    def _db_fetch(self, AccessGroupId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.AccessGroupId == AccessGroupId)
            result = self.data_access.connection.execute(s)
            row = result.first()

            if row == None:
                raise FetchError('The AccessGroup does not exist. AccessGroup Id is {0}.'.format(str(AccessGroupId)))
            else:
                #Get results and assign them to class variables

                self.AccessGroupId = row[0]
                self.Name = row[1]
                self.IsFetched = True

    def _db_delete_check(self):
        if self.IsDeleted:
            raise DeleteError('The AccessGroup is deleted.')

    def _db_delete(self):
        s = self.content.delete().where(self.content.c.AccessGroupId == self.AccessGroupId)
        self.data_access.connection.execute(s)

        self.IsDeleted = True

    def _db_update_check(self):
        if self.IsDeleted:
            raise UpdateError('The AccessGroup is deleted.')

    def _db_update(self):
        s = self.content.update().where(self.content.c.AccessGroupId == self.AccessGroupId).values(Name = self.Name)
        self.data_access.connection.execute(s)

        self.IsUpdated = True

class File(): 

    def __init__(self, FileId = None, Name = None, Path = None,  data_access = None):
        self.meta = MetaData()
        self.data_access = data_access

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsDeleted = False

        self.content = Table(
            'File', self.meta,
            Column('FileId', Integer, primary_key = True),
            Column('Name', String),
            Column('Path', String),
        )

        self.FileId = FileId
        self.Name = Name
        self.Path = Path
        
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

    def DBFetch(self, FileId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(FileId)
        except FetchError as fetch_error:
            raise fetch_error

    def Delete(self):
        try:
            if self.IsInserted or self.IsFetched:
                self._db_delete_check()
                self._db_delete()
            else:
                raise DeleteError('The File is neither fetched nor inserted.')
        except DeleteError as delete_error:
            raise delete_error

    def _db_insert_check(self):
        if self.IsDeleted:
            raise InsertError('The File is deleted.')

        if self.IsInserted:
            raise InsertError('The File has already been inserted.')

        if self.IsUpdated:
            raise InsertError('The File has been inserted.')

        if self.Name == None:
            raise InsertError('Please make sure that Name has a value.')

        if self.Path == None:
            raise InsertError('Please make sure that Path has a value.')

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'Name':self.Name, 'Path':self.Path},
            ])
            self.FileId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        if self.IsDeleted:
            raise FetchError('The File is deleted.')

    def _db_fetch(self, FileId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.FileId == FileId)
            result = self.data_access.connection.execute(s)
            row = result.first()

            if row == None:
                raise FetchError('The File does not exist. File Id is {0}.'.format(str(FileId)))
            else:
                #Get results and assign them to class variables

                self.FileId = row[0]
                self.Name = row[1]
                self.Path = row[2]
                self.IsFetched = True

    def _db_delete_check(self):
        if self.IsDeleted:
            raise DeleteError('The File is deleted.')

    def _db_delete(self):
        s = self.content.delete().where(self.content.c.FileId == self.FileId)
        self.data_access.connection.execute(s)

        self.IsDeleted = True

    def _db_update_check(self):
        if self.IsDeleted:
            raise UpdateError('The File is deleted.')

    def _db_update(self):
        s = self.content.update().where(self.content.c.FileId == self.FileId).values(Name = self.Name, Path = self.Path)
        self.data_access.connection.execute(s)

        self.IsUpdated = True


class FileAccess():

    def __init__(self, FileAccessId=None, FileId=None, AccessGroupId=None,  data_access=None):
        self.meta = MetaData()
        self.data_access = data_access

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsDeleted = False

        self.content = Table(
            'FileAccess', self.meta,
            Column('FileAccessId', Integer, primary_key=True),
            Column('FileId', Integer),
            Column('AccessGroupId', Integer),
        )

        self.FileAccessId = FileAccessId
        self.FileId = FileId
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

    def DBFetch(self, FileAccessId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(FileAccessId)
        except FetchError as fetch_error:
            raise fetch_error

    def Delete(self):
        try:
            if self.IsInserted or self.IsFetched:
                self._db_delete_check()
                self._db_delete()
            else:
                raise DeleteError(
                    'The FileAccess is neither fetched nor inserted.')
        except DeleteError as delete_error:
            raise delete_error

    def _db_insert_check(self):
        if self.IsDeleted:
            raise InsertError('The FileAccess is deleted.')

        if self.IsInserted:
            raise InsertError('The FileAccess has already been inserted.')

        if self.IsUpdated:
            raise InsertError('The FileAccess has been inserted.')

        if self.FileId == None:
            raise InsertError('Please make sure that FileId has a value.')

        if self.AccessGroupId == None:
            raise InsertError(
                'Please make sure that AccessGroupId has a value.')

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'FileId': self.FileId, 'AccessGroupId': self.AccessGroupId},
            ])
            self.FileAccessId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        if self.IsDeleted:
            raise FetchError('The FileAccess is deleted.')

    def _db_fetch(self, FileAccessId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.FileAccessId == FileAccessId)
            result = self.data_access.connection.execute(s)
            row = result.first()

            if row == None:
                raise FetchError(
                    'The FileAccess does not exist. FileAccess Id is {0}.'.format(str(FileAccessId)))
            else:
                #Get results and assign them to class variables

                self.FileAccessId = row[0]
                self.FileId = row[1]
                self.AccessGroupId = row[2]
                self.IsFetched = True

    def _db_delete_check(self):
        if self.IsDeleted:
            raise DeleteError('The FileAccess is deleted.')

    def _db_delete(self):
        s = self.content.delete().where(self.content.c.FileAccessId == self.FileAccessId)
        self.data_access.connection.execute(s)

        self.IsDeleted = True

    def _db_update_check(self):
        if self.IsDeleted:
            raise UpdateError('The FileAccess is deleted.')

    def _db_update(self):
        s = self.content.update().where(self.content.c.FileAccessId ==
                                        self.FileAccessId).values(FileId=self.FileId, AccessGroupId=self.AccessGroupId)
        self.data_access.connection.execute(s)

        self.IsUpdated = True

class Location(): 

    def __init__(self, LocationId = None, OnlineLink = None, Room = None, Building = None, Street = None, Town = None,  data_access = None):
        self.meta = MetaData()
        self.data_access = data_access

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsDeleted = False

        self.content = Table(
            'Location', self.meta,
            Column('LocationId', Integer, primary_key = True),
            Column('OnlineLink', String),
            Column('Room', String),
            Column('Building', String),
            Column('Street', String),
            Column('Town', String),
        )

        self.LocationId = LocationId
        self.OnlineLink = OnlineLink
        self.Room = Room
        self.Building = Building
        self.Street = Street
        self.Town = Town
        
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

    def DBFetch(self, LocationId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(LocationId)
        except FetchError as fetch_error:
            raise fetch_error

    def Delete(self):
        try:
            if self.IsInserted or self.IsFetched:
                self._db_delete_check()
                self._db_delete()
            else:
                raise DeleteError('The Location is neither fetched nor inserted.')
        except DeleteError as delete_error:
            raise delete_error

    def _db_insert_check(self):
        if self.IsDeleted:
            raise InsertError('The Location is deleted.')

        if self.IsInserted:
            raise InsertError('The Location has already been inserted.')

        if self.IsUpdated:
            raise InsertError('The Location has been inserted.')

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'OnlineLink':self.OnlineLink, 'Room':self.Room, 'Building':self.Building, 'Street':self.Street, 'Town':self.Town},
            ])
            self.LocationId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        if self.IsDeleted:
            raise FetchError('The Location is deleted.')

    def _db_fetch(self, LocationId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.LocationId == LocationId)
            result = self.data_access.connection.execute(s)
            row = result.first()

            if row == None:
                raise FetchError('The Location does not exist. Location Id is {0}.'.format(str(LocationId)))
            else:
                #Get results and assign them to class variables

                self.LocationId = row[0]
                self.OnlineLink = row[1]
                self.Room = row[2]
                self.Building = row[3]
                self.Street = row[4]
                self.Town = row[5]
                self.IsFetched = True

    def _db_delete_check(self):
        if self.IsDeleted:
            raise DeleteError('The Location is deleted.')

    def _db_delete(self):
        s = self.content.delete().where(self.content.c.LocationId == self.LocationId)
        self.data_access.connection.execute(s)

        self.IsDeleted = True

    def _db_update_check(self):
        if self.IsDeleted:
            raise UpdateError('The Location is deleted.')

    def _db_update(self):
        s = self.content.update().where(self.content.c.LocationId == self.LocationId).values(OnlineLink = self.OnlineLink, Room = self.Room, Building = self.Building, Street = self.Street, Town = self.Town)
        self.data_access.connection.execute(s)

        self.IsUpdated = True

class Meeting(): 

    def __init__(self, MeetingId = None, MeetingTypeId = None, HostId = None, LocationId = None, Title = None, StartDate = None, EndDate = None,  data_access = None):
        self.meta = MetaData()
        self.data_access = data_access

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsDeleted = False

        self.content = Table(
            'Meeting', self.meta,
            Column('MeetingId', Integer, primary_key = True),
            Column('MeetingTypeId', Integer),
            Column('HostId', Integer),
            Column('LocationId', Integer),
            Column('Title', String),
            Column('StartDate', DateTime),
            Column('EndDate', DateTime),
        )

        self.MeetingId = MeetingId
        self.MeetingTypeId = MeetingTypeId
        self.HostId = HostId
        self.LocationId = LocationId
        self.Title = Title
        self.StartDate = StartDate
        self.EndDate = EndDate
        
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

    def DBFetch(self, MeetingId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(MeetingId)
        except FetchError as fetch_error:
            raise fetch_error

    def Delete(self):
        try:
            if self.IsInserted or self.IsFetched:
                self._db_delete_check()
                self._db_delete()
            else:
                raise DeleteError('The Meeting is neither fetched nor inserted.')
        except DeleteError as delete_error:
            raise delete_error

    def _db_insert_check(self):
        if self.IsDeleted:
            raise InsertError('The Meeting is deleted.')

        if self.IsInserted:
            raise InsertError('The Meeting has already been inserted.')

        if self.IsUpdated:
            raise InsertError('The Meeting has been inserted.')

        if self.MeetingTypeId == None:
            raise InsertError('Please make sure that MeetingTypeId has a value.')

        if self.HostId == None:
            raise InsertError('Please make sure that HostId has a value.')

        if self.LocationId == None:
            raise InsertError('Please make sure that LocationId has a value.')

        if self.Title == None:
            raise InsertError('Please make sure that Title has a value.')

        if self.StartDate == None:
            raise InsertError('Please make sure that StartDate has a value.')

        if self.EndDate == None:
            raise InsertError('Please make sure that EndDate has a value.')

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'MeetingTypeId':self.MeetingTypeId, 'HostId':self.HostId, 'LocationId':self.LocationId, 'Title':self.Title, 'StartDate':self.StartDate, 'EndDate':self.EndDate},
            ])
            self.MeetingId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        if self.IsDeleted:
            raise FetchError('The Meeting is deleted.')

    def _db_fetch(self, MeetingId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.MeetingId == MeetingId)
            result = self.data_access.connection.execute(s)
            row = result.first()

            if row == None:
                raise FetchError('The Meeting does not exist. Meeting Id is {0}.'.format(str(MeetingId)))
            else:
                #Get results and assign them to class variables

                self.MeetingId = row[0]
                self.MeetingTypeId = row[1]
                self.HostId = row[2]
                self.LocationId = row[3]
                self.Title = row[4]
                self.StartDate = row[5]
                self.EndDate = row[6]
                self.IsFetched = True

    def _db_delete_check(self):
        if self.IsDeleted:
            raise DeleteError('The Meeting is deleted.')

    def _db_delete(self):
        s = self.content.delete().where(self.content.c.MeetingId == self.MeetingId)
        self.data_access.connection.execute(s)

        self.IsDeleted = True

    def _db_update_check(self):
        if self.IsDeleted:
            raise UpdateError('The Meeting is deleted.')

    def _db_update(self):
        s = self.content.update().where(self.content.c.MeetingId == self.MeetingId).values(MeetingTypeId = self.MeetingTypeId, HostId = self.HostId, LocationId = self.LocationId, Title = self.Title, StartDate = self.StartDate, EndDate = self.EndDate)
        self.data_access.connection.execute(s)

        self.IsUpdated = True

class MeetingAccess(): 

    def __init__(self, MeetingAccessId = None, MeetingId = None, AccessGroupId = None,  data_access = None):
        self.meta = MetaData()
        self.data_access = data_access

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsDeleted = False

        self.content = Table(
            'MeetingAccess', self.meta,
            Column('MeetingAccessId', Integer, primary_key = True),
            Column('MeetingId', Integer),
            Column('AccessGroupId', Integer),
        )

        self.MeetingAccessId = MeetingAccessId
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

    def DBFetch(self, MeetingAccessId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(MeetingAccessId)
        except FetchError as fetch_error:
            raise fetch_error

    def Delete(self):
        try:
            if self.IsInserted or self.IsFetched:
                self._db_delete_check()
                self._db_delete()
            else:
                raise DeleteError('The MeetingAccess is neither fetched nor inserted.')
        except DeleteError as delete_error:
            raise delete_error

    def _db_insert_check(self):
        if self.IsDeleted:
            raise InsertError('The MeetingAccess is deleted.')

        if self.IsInserted:
            raise InsertError('The MeetingAccess has already been inserted.')

        if self.IsUpdated:
            raise InsertError('The MeetingAccess has been inserted.')

        if self.MeetingId == None:
            raise InsertError('Please make sure that MeetingId has a value.')

        if self.AccessGroupId == None:
            raise InsertError('Please make sure that AccessGroupId has a value.')

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'MeetingId':self.MeetingId, 'AccessGroupId':self.AccessGroupId},
            ])
            self.MeetingAccessId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        if self.IsDeleted:
            raise FetchError('The MeetingAccess is deleted.')

    def _db_fetch(self, MeetingAccessId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.MeetingAccessId == MeetingAccessId)
            result = self.data_access.connection.execute(s)
            row = result.first()

            if row == None:
                raise FetchError('The MeetingAccess does not exist. MeetingAccess Id is {0}.'.format(str(MeetingAccessId)))
            else:
                #Get results and assign them to class variables

                self.MeetingAccessId = row[0]
                self.MeetingId = row[1]
                self.AccessGroupId = row[2]
                self.IsFetched = True

    def _db_delete_check(self):
        if self.IsDeleted:
            raise DeleteError('The MeetingAccess is deleted.')

    def _db_delete(self):
        s = self.content.delete().where(self.content.c.MeetingAccessId == self.MeetingAccessId)
        self.data_access.connection.execute(s)

        self.IsDeleted = True

    def _db_update_check(self):
        if self.IsDeleted:
            raise UpdateError('The MeetingAccess is deleted.')

    def _db_update(self):
        s = self.content.update().where(self.content.c.MeetingAccessId == self.MeetingAccessId).values(MeetingId = self.MeetingId, AccessGroupId = self.AccessGroupId)
        self.data_access.connection.execute(s)

        self.IsUpdated = True

class MeetingFile(): 

    def __init__(self, MeetingFileId = None, MeetingId = None, FileId = None,  data_access = None):
        self.meta = MetaData()
        self.data_access = data_access

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsDeleted = False

        self.content = Table(
            'MeetingFile', self.meta,
            Column('MeetingFileId', Integer, primary_key = True),
            Column('MeetingId', Integer),
            Column('FileId', Integer),
        )

        self.MeetingFileId = MeetingFileId
        self.MeetingId = MeetingId
        self.FileId = FileId
        
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

    def DBFetch(self, MeetingFileId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(MeetingFileId)
        except FetchError as fetch_error:
            raise fetch_error

    def Delete(self):
        try:
            if self.IsInserted or self.IsFetched:
                self._db_delete_check()
                self._db_delete()
            else:
                raise DeleteError('The MeetingFile is neither fetched nor inserted.')
        except DeleteError as delete_error:
            raise delete_error

    def _db_insert_check(self):
        if self.IsDeleted:
            raise InsertError('The MeetingFile is deleted.')

        if self.IsInserted:
            raise InsertError('The MeetingFile has already been inserted.')

        if self.IsUpdated:
            raise InsertError('The MeetingFile has been inserted.')

        if self.MeetingId == None:
            raise InsertError('Please make sure that MeetingId has a value.')

        if self.FileId == None:
            raise InsertError('Please make sure that FileId has a value.')

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'MeetingId':self.MeetingId, 'FileId':self.FileId},
            ])
            self.MeetingFileId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        if self.IsDeleted:
            raise FetchError('The MeetingFile is deleted.')

    def _db_fetch(self, MeetingFileId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.MeetingFileId == MeetingFileId)
            result = self.data_access.connection.execute(s)
            row = result.first()

            if row == None:
                raise FetchError('The MeetingFile does not exist. MeetingFile Id is {0}.'.format(str(MeetingFileId)))
            else:
                #Get results and assign them to class variables

                self.MeetingFileId = row[0]
                self.MeetingId = row[1]
                self.FileId = row[2]
                self.IsFetched = True

    def _db_delete_check(self):
        if self.IsDeleted:
            raise DeleteError('The MeetingFile is deleted.')

    def _db_delete(self):
        s = self.content.delete().where(self.content.c.MeetingFileId == self.MeetingFileId)
        self.data_access.connection.execute(s)

        self.IsDeleted = True

    def _db_update_check(self):
        if self.IsDeleted:
            raise UpdateError('The MeetingFile is deleted.')

    def _db_update(self):
        s = self.content.update().where(self.content.c.MeetingFileId == self.MeetingFileId).values(MeetingId = self.MeetingId, FileId = self.FileId)
        self.data_access.connection.execute(s)

        self.IsUpdated = True


class MeetingInvitation():

    def __init__(self, MeetingInvitationId=None, MeetingId=None, AccessGroupId=None,  data_access=None):
        self.meta = MetaData()
        self.data_access = data_access

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsDeleted = False

        self.content = Table(
            'MeetingInvitation', self.meta,
            Column('MeetingInvitationId', Integer, primary_key=True),
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
                raise DeleteError(
                    'The MeetingInvitation is neither fetched nor inserted.')
        except DeleteError as delete_error:
            raise delete_error

    def _db_insert_check(self):
        if self.IsDeleted:
            raise InsertError('The MeetingInvitation is deleted.')

        if self.IsInserted:
            raise InsertError(
                'The MeetingInvitation has already been inserted.')

        if self.IsUpdated:
            raise InsertError('The MeetingInvitation has been inserted.')

        if self.MeetingId == None:
            raise InsertError('Please make sure that MeetingId has a value.')

        if self.AccessGroupId == None:
            raise InsertError(
                'Please make sure that AccessGroupId has a value.')

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'MeetingId': self.MeetingId, 'AccessGroupId': self.AccessGroupId},
            ])
            self.MeetingInvitationId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        if self.IsDeleted:
            raise FetchError('The MeetingInvitation is deleted.')

    def _db_fetch(self, MeetingInvitationId):
        if not self.IsFetched:
            s = self.content.select().where(
                self.content.c.MeetingInvitationId == MeetingInvitationId)
            result = self.data_access.connection.execute(s)
            row = result.first()

            if row == None:
                raise FetchError('The MeetingInvitation does not exist. MeetingInvitation Id is {0}.'.format(
                    str(MeetingInvitationId)))
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
        s = self.content.delete().where(
            self.content.c.MeetingInvitationId == self.MeetingInvitationId)
        self.data_access.connection.execute(s)

        self.IsDeleted = True

    def _db_update_check(self):
        if self.IsDeleted:
            raise UpdateError('The MeetingInvitation is deleted.')

    def _db_update(self):
        s = self.content.update().where(self.content.c.MeetingInvitationId ==
                                        self.MeetingInvitationId).values(MeetingId=self.MeetingId, AccessGroupId=self.AccessGroupId)
        self.data_access.connection.execute(s)

        self.IsUpdated = True


class MeetingType(): 

    def __init__(self, MeetingTypeId = None, Name = None,  data_access = None):
        self.meta = MetaData()
        self.data_access = data_access

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsDeleted = False

        self.content = Table(
            'MeetingType', self.meta,
            Column('MeetingTypeId', Integer, primary_key = True),
            Column('Name', String),
        )

        self.MeetingTypeId = MeetingTypeId
        self.Name = Name
        
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

    def DBFetch(self, MeetingTypeId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(MeetingTypeId)
        except FetchError as fetch_error:
            raise fetch_error

    def Delete(self):
        try:
            if self.IsInserted or self.IsFetched:
                self._db_delete_check()
                self._db_delete()
            else:
                raise DeleteError('The MeetingType is neither fetched nor inserted.')
        except DeleteError as delete_error:
            raise delete_error

    def _db_insert_check(self):
        if self.IsDeleted:
            raise InsertError('The MeetingType is deleted.')

        if self.IsInserted:
            raise InsertError('The MeetingType has already been inserted.')

        if self.IsUpdated:
            raise InsertError('The MeetingType has been inserted.')

        if self.Name == None:
            raise InsertError('Please make sure that Name has a value.')

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'Name':self.Name},
            ])
            self.MeetingTypeId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        if self.IsDeleted:
            raise FetchError('The MeetingType is deleted.')

    def _db_fetch(self, MeetingTypeId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.MeetingTypeId == MeetingTypeId)
            result = self.data_access.connection.execute(s)
            row = result.first()

            if row == None:
                raise FetchError('The MeetingType does not exist. MeetingType Id is {0}.'.format(str(MeetingTypeId)))
            else:
                #Get results and assign them to class variables

                self.MeetingTypeId = row[0]
                self.Name = row[1]
                self.IsFetched = True

    def _db_delete_check(self):
        if self.IsDeleted:
            raise DeleteError('The MeetingType is deleted.')

    def _db_delete(self):
        s = self.content.delete().where(self.content.c.MeetingTypeId == self.MeetingTypeId)
        self.data_access.connection.execute(s)

        self.IsDeleted = True

    def _db_update_check(self):
        if self.IsDeleted:
            raise UpdateError('The MeetingType is deleted.')

    def _db_update(self):
        s = self.content.update().where(self.content.c.MeetingTypeId == self.MeetingTypeId).values(Name = self.Name)
        self.data_access.connection.execute(s)

        self.IsUpdated = True

class User(): 

    def __init__(self, UserId = None, Email = None, Password = None, Firstname = None, Lastname = None, RegistrationDate = None, LastAccessDate = None, UniqueLogins = None, PasswordRecovery = None,  data_access = None):
        self.meta = MetaData()
        self.data_access = data_access

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsDeleted = False

        self.content = Table(
            'User', self.meta,
            Column('UserId', Integer, primary_key = True),
            Column('Email', String),
            Column('Password', String),
            Column('Firstname', String),
            Column('Lastname', String),
            Column('RegistrationDate', DateTime),
            Column('LastAccessDate', DateTime),
            Column('UniqueLogins', Integer),
            Column('PasswordRecovery', String),
        )

        self.UserId = UserId
        self.Email = Email
        self.Password = Password
        self.Firstname = Firstname
        self.Lastname = Lastname
        self.RegistrationDate = RegistrationDate
        self.LastAccessDate = LastAccessDate
        self.UniqueLogins = UniqueLogins
        self.PasswordRecovery = PasswordRecovery
        
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

    def DBFetch(self, UserId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(UserId)
        except FetchError as fetch_error:
            raise fetch_error

    def Delete(self):
        try:
            if self.IsInserted or self.IsFetched:
                self._db_delete_check()
                self._db_delete()
            else:
                raise DeleteError('The User is neither fetched nor inserted.')
        except DeleteError as delete_error:
            raise delete_error

    def _db_insert_check(self):
        if self.IsDeleted:
            raise InsertError('The User is deleted.')

        if self.IsInserted:
            raise InsertError('The User has already been inserted.')

        if self.IsUpdated:
            raise InsertError('The User has been inserted.')

        if self.Email == None:
            raise InsertError('Please make sure that Email has a value.')

        if self.Password == None:
            raise InsertError('Please make sure that Password has a value.')

        if self.Firstname == None:
            raise InsertError('Please make sure that Firstname has a value.')

        if self.Lastname == None:
            raise InsertError('Please make sure that Lastname has a value.')

        if self.RegistrationDate == None:
            raise InsertError('Please make sure that RegistrationDate has a value.')

        if self.UniqueLogins == None:
            raise InsertError('Please make sure that UniqueLogins has a value.')

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'Email':self.Email, 'Password':self.Password, 'Firstname':self.Firstname, 'Lastname':self.Lastname, 'RegistrationDate':self.RegistrationDate, 'LastAccessDate':self.LastAccessDate, 'UniqueLogins':self.UniqueLogins, 'PasswordRecovery':self.PasswordRecovery},
            ])
            self.UserId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        if self.IsDeleted:
            raise FetchError('The User is deleted.')

    def _db_fetch(self, UserId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.UserId == UserId)
            result = self.data_access.connection.execute(s)
            row = result.first()

            if row == None:
                raise FetchError('The User does not exist. User Id is {0}.'.format(str(UserId)))
            else:
                #Get results and assign them to class variables

                self.UserId = row[0]
                self.Email = row[1]
                self.Password = row[2]
                self.Firstname = row[3]
                self.Lastname = row[4]
                self.RegistrationDate = row[5]
                self.LastAccessDate = row[6]
                self.UniqueLogins = row[7]
                self.PasswordRecovery = row[8]
                self.IsFetched = True

    def _db_delete_check(self):
        if self.IsDeleted:
            raise DeleteError('The User is deleted.')

    def _db_delete(self):
        s = self.content.delete().where(self.content.c.UserId == self.UserId)
        self.data_access.connection.execute(s)

        self.IsDeleted = True

    def _db_update_check(self):
        if self.IsDeleted:
            raise UpdateError('The User is deleted.')

    def _db_update(self):
        s = self.content.update().where(self.content.c.UserId == self.UserId).values(Email = self.Email, Password = self.Password, Firstname = self.Firstname, Lastname = self.Lastname, RegistrationDate = self.RegistrationDate, LastAccessDate = self.LastAccessDate, UniqueLogins = self.UniqueLogins, PasswordRecovery = self.PasswordRecovery)
        self.data_access.connection.execute(s)

        self.IsUpdated = True

class UserAccessGroup(): 

    def __init__(self, UserAccessGroupId = None, UserId = None, AccessGroupId = None,  data_access = None):
        self.meta = MetaData()
        self.data_access = data_access

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsDeleted = False

        self.content = Table(
            'UserAccessGroup', self.meta,
            Column('UserAccessGroupId', Integer, primary_key = True),
            Column('UserId', Integer),
            Column('AccessGroupId', Integer),
        )

        self.UserAccessGroupId = UserAccessGroupId
        self.UserId = UserId
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

    def DBFetch(self, UserAccessGroupId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(UserAccessGroupId)
        except FetchError as fetch_error:
            raise fetch_error

    def Delete(self):
        try:
            if self.IsInserted or self.IsFetched:
                self._db_delete_check()
                self._db_delete()
            else:
                raise DeleteError('The UserAccessGroup is neither fetched nor inserted.')
        except DeleteError as delete_error:
            raise delete_error

    def _db_insert_check(self):
        if self.IsDeleted:
            raise InsertError('The UserAccessGroup is deleted.')

        if self.IsInserted:
            raise InsertError('The UserAccessGroup has already been inserted.')

        if self.IsUpdated:
            raise InsertError('The UserAccessGroup has been inserted.')

        if self.UserId == None:
            raise InsertError('Please make sure that UserId has a value.')

        if self.AccessGroupId == None:
            raise InsertError('Please make sure that AccessGroupId has a value.')

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'UserId':self.UserId, 'AccessGroupId':self.AccessGroupId},
            ])
            self.UserAccessGroupId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        if self.IsDeleted:
            raise FetchError('The UserAccessGroup is deleted.')

    def _db_fetch(self, UserAccessGroupId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.UserAccessGroupId == UserAccessGroupId)
            result = self.data_access.connection.execute(s)
            row = result.first()

            if row == None:
                raise FetchError('The UserAccessGroup does not exist. UserAccessGroup Id is {0}.'.format(str(UserAccessGroupId)))
            else:
                #Get results and assign them to class variables

                self.UserAccessGroupId = row[0]
                self.UserId = row[1]
                self.AccessGroupId = row[2]
                self.IsFetched = True

    def _db_delete_check(self):
        if self.IsDeleted:
            raise DeleteError('The UserAccessGroup is deleted.')

    def _db_delete(self):
        s = self.content.delete().where(self.content.c.UserAccessGroupId == self.UserAccessGroupId)
        self.data_access.connection.execute(s)

        self.IsDeleted = True

    def _db_update_check(self):
        if self.IsDeleted:
            raise UpdateError('The UserAccessGroup is deleted.')

    def _db_update(self):
        s = self.content.update().where(self.content.c.UserAccessGroupId == self.UserAccessGroupId).values(UserId = self.UserId, AccessGroupId = self.AccessGroupId)
        self.data_access.connection.execute(s)

        self.IsUpdated = True
