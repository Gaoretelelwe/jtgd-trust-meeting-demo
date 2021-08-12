from Util.Encryption import AESCipher
from Util.ErrorHandler import InsertError, UpdateError, DeleteError, FetchError, LoginError
from Util.StoredProcs import StoredProcs

from sqlalchemy import Table, Column, Integer, String, Float, DateTime, MetaData, and_
from DataAccess.DataAccess import DataAccess

#from Objects.DataObjects.Vendor import Vendor

from system_config import SystemConfig

import pdb #debugging tool -- pdb.set_trace()  

# HelloPass123

class LoginLogic:

    def __init__(self, email, password, data_access):
        self.LoginMessage = ''
        self.Email = email
        self.Password = password
        self.UserId = None
        self.IsLogged = False
        self.IsLoginError = False
        self.LoggedEntity = None
        self.meta = MetaData()
        self.data_access = data_access

        self.user_content = Table(
            'User', self.meta,
            Column('UserId', Integer, primary_key = True), 
            Column('Email', String),
            Column('Password', String),
            Column('Firstname', String), 
            Column('Lastname', String), 
        )
    
    def _set_login_message(self, LoginMessage):
        self.LoginMessage = LoginMessage

    def _set_login_error(self, IsLoginError):
        self.IsLoginError = IsLoginError
    
    def _set_login_entity(self):
        # Login Entity = Vendor / Admin / Super Admin
        # Password = row[2]
        sysConfig = SystemConfig()
        aes = AESCipher(sysConfig.ENCRYPTION_KEY)

        #s = self.admin_content.select().where(and_(self.admin_content.c.EmailAddress == self.Email, 
        #                                           self.admin_content.c.Password == self.Password))

        ### Can select with EmailAddress only since EmailAddress is a Unique Column on the database
        s = self.user_content.select().where(and_(self.user_content.c.Email == self.Email))
        result = self.data_access.connection.execute(s)
        row = result.first()

        if row != None: 
            
            userPassword = aes.decrypt(row[2])
            
            if userPassword == self.Password: 
                self.UserId = row[0]
                
                storedProc = StoredProcs()
                    
                if storedProc.isAdminUser(self.UserId, self.data_access): self.LoggedEntity = 'ADMIN'
                else: self.LoggedEntity = None
                self._set_login_error(False)
            else:
                self._set_login_message('Incorrect email address or password.')
                self._set_login_error(True)
        else: 
            self._set_login_message('Incorrect email address or password.')
            self._set_login_error(True)


    def GetLoginMessage(self):
        return self.LoginMessage

    def Login(self):
        try:
            if not self.IsLogged:
                self._set_login_entity()
                self._login_check()
                self._login()
        except LoginError as login_error:
            raise login_error
    
    def _login_check(self):
        if self.IsLoginError:
            raise LoginError(self.LoginMessage)
    
    def _login(self):
        self.IsLogged = True
