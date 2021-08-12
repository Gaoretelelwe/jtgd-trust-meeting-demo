
from Util.ErrorHandler import InsertError, UpdateError, DeleteError, FetchError, RecoverPasswordError

from sqlalchemy import Table, Column, Integer, String, Float, DateTime, MetaData, and_
from DataAccess.DataAccess import DataAccess

#from Objects.DataObjects.Vendor import Vendor

import pdb #debugging tool -- pdb.set_trace()

class RecoverPasswordLogic:

    def __init__(self, email, data_access):
        self.RecoverPasswordMessage = ''
        self.Email = email
        self.UserId = None
        self.IsRecovered = False
        self.IsRecoverPasswordError = False
        self.RecoveredEntity = None
        self.meta = MetaData()
        self.data_access = data_access

        self.user_content = Table(
            'User', self.meta,
            Column('UserId', Integer, primary_key = True),
            Column('Email', String),
            Column('PasswordRecovery', String),
        )
    
    def _set_recoverpassword_message(self, RecoverPasswordMessage):
        self.RecoverPasswordMessage = RecoverPasswordMessage

    def _set_recoverpassword_error(self, IsRecoverPasswordError):
        self.IsRecoverPasswordError = IsRecoverPasswordError
    
    def _set_recoverpassword_entity(self):
        # RecoverPassword Entity = Vendor / Admin / Super Admin

        s = self.user_content.select().where(self.user_content.c.Email == self.Email)
        result = self.data_access.connection.execute(s)
        row = result.first()
        
        if row != None:
            self.RecoveredEntity = 'User'
            self.UserId = row[0]
            self._set_recoverpassword_error(False)
        else:
            self._set_recoverpassword_message('Incorrect email address.')
            self._set_recoverpassword_error(True)


    def GetRecoverPasswordMessage(self):
        return self.RecoverPasswordMessage

    def RecoverPassword(self):
        try:
            if not self.IsRecovered:
                self._set_recoverpassword_entity()
                self._recoverpassword_check()
                self._recoverpassword()
        except RecoverPasswordError as recoverpassword_error:
            raise recoverpassword_error
    
    def _recoverpassword_check(self):
        if self.IsRecoverPasswordError:
            raise RecoverPasswordError(self.RecoverPasswordMessage)
    
    def _recoverpassword(self):
        self.IsRecovered = True